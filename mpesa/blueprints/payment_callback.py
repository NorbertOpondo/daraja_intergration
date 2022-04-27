from turtle import update
from flask import Blueprint, request, jsonify
import logging
from mpesa.models.payment import Payment, db
from mpesa.utils.payment_status import PaymentStatus

payment_callback = Blueprint('payment_callback', __name__)

LOG = logging.getLogger(__name__)

@payment_callback.route("/payment_callback", methods=['POST'])
def handle_payment_callback():
    ''' Receives payment callback from daraja API '''

    LOG.info("Received payment callback %s", request.json)

    callback_request = request.json
    result_code = callback_request["Body"]["stkCallback"]["ResultCode"]
    checkout_request_id = callback_request['Body']['stkCallback']['CheckoutRequestID']
    if result_code == 0:
        # successful payment
        mpesa_receipt_number = callback_request["Body"]["stkCallback"]["CallbackMetadata"]["Item"][1]["Value"]
        amount = callback_request["Body"]["stkCallback"]["CallbackMetadata"]["Item"][0]["Value"]
        phone_number = callback_request["Body"]["stkCallback"]["CallbackMetadata"]["Item"][3]["Value"]

        try:
            payment = Payment.query.filter(Payment.checkout_request_id == checkout_request_id).first()
            payment.amount = amount
            payment.payment_status = PaymentStatus.complete.name
            payment.mpesa_receipt_number = mpesa_receipt_number
            payment.callback_data = callback_request

            db.session.commit()
        except:
            db.session.rollback()
            raise
    else:
        try:
            payment = Payment.query.filter(Payment.checkout_request_id == checkout_request_id).first()
            payment.payment_status = PaymentStatus.failed.name
            payment.callback_data = callback_request
        
            db.session.commit()
        except:
            db.session.rollback()
            raise

    return jsonify({
		'message':'received',
		'status':'200'
	}),200
    

@payment_callback.route('/fetch_payments', methods=['GET'])
def fetch_payments():
    payments = Payment.query.all()
    data = []
    total_amount_collected = 0
    failed_transactions = 0
    
    for p in payments:
        data.append(p.to_dict())
        if p.to_dict()['payment_status'] == PaymentStatus.complete.name:
            total_amount_collected += p.to_dict()['amount']
        if p.to_dict()['payment_status'] == PaymentStatus.failed.name:
            failed_transactions += 1
    
    

    response = {
        'message' : 'success',
        'data' : data,
        'total_amount_collected' : total_amount_collected,
        'total_transactions' : len(payments),
        'failed_transactions' : failed_transactions
    }

    return jsonify(response),200
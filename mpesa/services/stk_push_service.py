import base64
import datetime
import logging
from mpesa.models.payment import Payment, db
from mpesa.services.intergrations.daraja_api_integration import get_access_token, daraja_initiage_stk_push
from mpesa.utils.payment_status import PaymentStatus
from flask import current_app

LOG = logging.getLogger(__name__)

def initialize_stk_push(phone_number, amount):
    ''' sends stk push request to safaricom API '''

    business_short_code = current_app.config['MPESA_BUSINESS_SHORT_CODE']
    pass_key = current_app.config["DARAJA_PASS_KEY"]
    current_timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
   
    string_to_encode = business_short_code+pass_key+current_timestamp
    byte_string = string_to_encode.encode()
    password = base64.b64encode(byte_string)

    request_body = {
        'BusinessShortCode': business_short_code,
        'Password': password.decode(),
        'Timestamp': current_timestamp,
        'TransactionType': 'CustomerPayBillOnline',    
        'Amount': amount,
        'PartyA': phone_number,
        'PartyB': business_short_code,    
        'PhoneNumber': phone_number,    
        'CallBackURL': current_app.config['CALLBACK_URL'],    
        'AccountReference': 'Nywele nyumbani',    
        'TransactionDesc':'Nyewele'
    }
    
    access_token = get_access_token()

    if access_token is None:
        raise Exception("Could not get access token")

    try:
        response =  daraja_initiage_stk_push(access_token, request_body)
        json_response = response.json()
        print(response.text)
        
        checkout_request_id = json_response['CheckoutRequestID']
        payment = Payment(phone_number=phone_number, amount=amount, payment_status=PaymentStatus.pending.name, checkout_request_id=checkout_request_id)
        db.session.add(payment)
        db.session.commit()
        return True
    except:
        db.session.rollback()
        raise

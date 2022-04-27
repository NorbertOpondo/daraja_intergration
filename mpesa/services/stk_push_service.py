import base64
import requests
import datetime
import logging
from mpesa.models.payment import Payment, db
from mpesa.utils.payment_status import PaymentStatus
from flask import current_app

LOG = logging.getLogger(__name__)

def initialize_stk_push(phone_number, amount):
    ''' sends stk push request to safaricom API '''

    business_short_code = '174379'
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
        'CallBackURL': 'https://53e2-102-140-196-253.ngrok.io/payment_callback',    
        'AccountReference': 'Nywele nyumbani',    
        'TransactionDesc':'ERQ78H6R'
    }

    LOG.info("request to daraja API %s", request_body)
    url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
    
    access_token = get_access_token()

    if access_token is None:
        raise Exception("Could not get access token")

    header = {
        'Authorization': 'Bearer ' +access_token
        }

    try:
        response = requests.post(url, headers=header, json=request_body)
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

def get_access_token():
    ''' Gets Authorization access token from DARAJA '''

    consumer_key = current_app.config['DARAJA_CONSUMER_KEY']
    consumer_secret = current_app.config['DARAJA_CONSUMER_SECRET']

    string_to_encode = consumer_key+':'+consumer_secret
    byte_string = string_to_encode.encode()
    encoded_byte_string = base64.b64encode(byte_string)
    
    url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    header = {
        'Authorization' : 'Basic ' +encoded_byte_string.decode()
    }
    response = requests.get(url, headers = header)

    json_response = response.json()
    
    return json_response['access_token']
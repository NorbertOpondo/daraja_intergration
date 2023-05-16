from flask import current_app
import base64
import requests
import logging

LOG = logging.getLogger(__name__)

def daraja_initiage_stk_push(access_token, request_body, ):
    ''' Makes an http call to DARAJA API to send an stk push to the 
    customer's phone'''

    LOG.info("request to daraja API %s", request_body)
    url = current_app.config['DARAJA_STK_PUSH_URL']

    header = {
        'Authorization': 'Bearer ' +access_token
        }

    response = requests.post(url, headers=header, json=request_body)

    return response


def get_access_token():
    ''' Gets Authorization Access Token from DARAJA API'''

    consumer_key = current_app.config['DARAJA_CONSUMER_KEY']
    consumer_secret = current_app.config['DARAJA_CONSUMER_SECRET']

    string_to_encode = consumer_key+':'+consumer_secret
    byte_string = string_to_encode.encode()
    encoded_byte_string = base64.b64encode(byte_string)
    
    url = current_app.config['DARAJA_AUTH_TOKEN_URL']

    print("encoded stuff",encoded_byte_string.decode())
    header = {
        'Authorization' : 'Basic ' +encoded_byte_string.decode()
    }
    response = requests.get(url, headers = header)

    print("get token response", response)
    json_response = response.json()
    
    return json_response['access_token']
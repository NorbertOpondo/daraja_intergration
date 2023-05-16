from distutils.log import debug
import os


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DB_CONNECTION_STRING')
    debug = True
    DARAJA_CONSUMER_KEY = os.getenv('DARAJA_CONSUMER_KEY')
    DARAJA_CONSUMER_SECRET = os.getenv('DARAJA_CONSUMER_SECRET')
    DARAJA_PASS_KEY = os.getenv('DARAJA_PASS_KEY')
    MPESA_BUSINESS_SHORT_CODE = '174379'
    CALLBACK_URL =  "https://81b8-196-207-151-57.ngrok.io/payment_callback"
    DARAJA_STK_PUSH_URL = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
    DARAJA_AUTH_TOKEN_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"


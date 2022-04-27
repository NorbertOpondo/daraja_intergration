from distutils.log import debug
import os


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@localhost/nywele_db'
    debug = True
    DARAJA_CONSUMER_KEY = os.getenv('DARAJA_CONSUMER_KEY')
    DARAJA_CONSUMER_SECRET = os.getenv('DARAJA_CONSUMER_SECRET')
    DARAJA_PASS_KEY = os.getenv('DARAJA_PASS_KEY')

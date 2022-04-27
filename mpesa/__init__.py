from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config
import logging

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)
    db.init_app(app)

    #Register the blueprints
    from mpesa.blueprints.initiate_stk_push import initiate_stk_blueprint;
    from mpesa.blueprints.payment_callback import payment_callback;

    app.register_blueprint(initiate_stk_blueprint)
    app.register_blueprint(payment_callback)

    # register root logging
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('werkzeug').setLevel(logging.INFO)

    return app

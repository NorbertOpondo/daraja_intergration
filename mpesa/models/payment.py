from mpesa import db
from datetime import datetime
from sqlalchemy_serializer import SerializerMixin

class Payment(db.Model, SerializerMixin):

    serialize_only = ('id', 'phone_number', 'amount', 'date_created', 'payment_status', 'checkout_request_id', 'mpesa_receipt_number')

    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.Float, nullable=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    payment_status = db.Column(db.String(10), nullable=False)
    checkout_request_id = db.Column(db.String(100), nullable=False)
    mpesa_receipt_number = db.Column(db.String(100), nullable=True)
    callback_data = db.Column(db.JSON, nullable=True)
    
    

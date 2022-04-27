import logging
from flask import Blueprint, request, jsonify, current_app
from mpesa.services.stk_push_service import initialize_stk_push

initiate_stk_blueprint = Blueprint('initiate_stk_blueprint', __name__)

LOG = logging.getLogger(__name__)

@initiate_stk_blueprint.route("/initiate_stk_push", methods=['POST'])
def initiate_stk_push():
    ''' Inititates an stk push'''

    request_body = request.json
    LOG.info("Received stk request %s", request_body)

    phone_number = request_body["phone_number"]
    amount = request_body["amount"]

    try:
      phone_number = int(phone_number)
      amount = int(amount)
      initialize_stk_push(phone_number, amount)
      message = {
        'message':'success',
        'status':'200'
	    }

      return jsonify(message),200
    except Exception as e:
      raise e
      message = {
        'message':str(e),
        'status':'500'
	    }
      return jsonify(message),500


    

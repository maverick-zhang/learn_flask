from flask import Blueprint

second = Blueprint("second", __name__)

@second.route('/list', methods=['POST', 'GET'])
def list():
    pass
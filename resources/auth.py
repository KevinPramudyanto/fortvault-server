from flask import Blueprint

auth = Blueprint('auth',__name__)

@auth.route('/', methods=['GET'])
def index():
    return 'Hello World!'
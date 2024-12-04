import os
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from resources.auth import auth

app = Flask(__name__)
CORS(app)
app.config['JWT_SECRET_KEY'] = os.environ['JWT_SECRET_KEY']
jwt = JWTManager(app)

app.register_blueprint(auth)

if __name__ == '__main__':
    app.run(port=5001,debug=True)

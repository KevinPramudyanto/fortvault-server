import os
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from resources.seed import seed
from resources.auth import auth
from resources.tool import tool
from resources.user import user
from resources.logs import logs

app = Flask(__name__)
CORS(app)
app.config['JWT_SECRET_KEY'] = os.environ['JWT_SECRET_KEY']
jwt = JWTManager(app)

app.register_blueprint(seed)
app.register_blueprint(auth)
app.register_blueprint(tool)
app.register_blueprint(user)
app.register_blueprint(logs)

if __name__ == '__main__':
    app.run(port=5001, debug=True)

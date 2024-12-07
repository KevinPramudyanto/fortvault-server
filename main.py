import os
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO
from resources.auth import auth
from resources.tool import tool
from resources.user import user

app = Flask(__name__)
CORS(app)
app.config['JWT_SECRET_KEY'] = os.environ['JWT_SECRET_KEY']
jwt = JWTManager(app)
socketio = SocketIO(app, cors_allowed_origins="*")

app.register_blueprint(auth)
app.register_blueprint(tool)
app.register_blueprint(user)

@socketio.on('message')
def handle_message(input):
    print('received message: ' + input)
    socketio.emit('message', input)

if __name__ == '__main__':
    socketio.run(app, port=5001, debug=True, allow_unsafe_werkzeug=True)

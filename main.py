from flask import Flask
from resources.auth import auth

app = Flask(__name__)

app.register_blueprint(auth)

if __name__ == '__main__':
    app.run(port=5001,debug=True)

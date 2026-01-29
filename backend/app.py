#app.py

from flask import Flask
from application.config import Config, LocalConfig, ProductionConfig
from flask_restful import Api
from application.database import db
import os 
from dotenv import load_dotenv
from flask_cors import CORS
from flask_jwt_extended import JWTManager

load_dotenv()

app = None 
api = None
jwt = None
def create_app():
    app = Flask(__name__)
    if os.getenv('env') == 'local':
        print("Starting Local Environment")
        app.config.from_object(LocalConfig)
    db.init_app(app)
    api = Api(app)
    jwt = JWTManager(app)
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})
    app.app_context().push()
    return app , api 

app, api = create_app()



from application.controllers import * 
from application.api import *


api.add_resource(UserAPI, "/api/user/<string:username>", "/api/user")
api.add_resource(LoginAPI, "/api/login") 
api.add_resource(RegisterAPI, "/api/register")



if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
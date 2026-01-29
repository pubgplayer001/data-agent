from flask import current_app as app 
from application.models import User



@app.route("/") 
def home():
    return "Hello"
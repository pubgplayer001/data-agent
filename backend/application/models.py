# application/models.py
from application.database import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'user'
    username = db.Column(db.String(80), primary_key=True)  # unique identifier
    name = db.Column(db.String(120), nullable=False)       # full name
    email = db.Column(db.String(120), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=True)
    password_hash = db.Column(db.String(128), nullable=False)  # store hashed password
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def as_dict(self):
        return {
            "username": self.username,
            "name": self.name,
            "email": self.email,
            "age": self.age
        }

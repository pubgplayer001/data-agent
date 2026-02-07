# application/models.py
from application.database import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

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


class Conversations(db.Model):
    __tablename__ = 'conversations'
    conversation_id = db.Column(db.String(120), primary_key=True)
    user_id = db.Column(db.String(80), db.ForeignKey('user.username'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationship with Messages
    messages = db.relationship('Messages', backref='conversation', cascade="all, delete-orphan", lazy=True)

    def as_dict(self):
        return {
            "conversation_id": self.conversation_id,
            "user_id": self.user_id,
            "title": self.title,
            "created_at": self.created_at,
            "messages": [message.as_dict() for message in self.messages]
        }


class Messages(db.Model):
    __tablename__ = 'messages'
    message_id = db.Column(db.String(120), primary_key=True)
    conversation_id = db.Column(db.String(120), db.ForeignKey('conversations.conversation_id'), nullable=False)
    sender = db.Column(db.String(10), nullable=False)  # 'user' or 'bot'
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def as_dict(self):
        return {
            "message_id": self.message_id,
            "conversation_id": self.conversation_id,
            "sender": self.sender,
            "message": self.message,
            "timestamp": self.timestamp
        }
    
class Files(db.Model):
    __tablename__ = 'files'
    file_id = db.Column(db.String(120), primary_key=True)
    user_id = db.Column(db.String(80), db.ForeignKey('user.username'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    filepath = db.Column(db.String(255), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def as_dict(self):
        return {
            "file_id": self.file_id,
            "user_id": self.user_id,
            "filename": self.filename,
            "filepath": self.filepath,
            "uploaded_at": self.uploaded_at
        }
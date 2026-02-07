from flask_restful import Resource 
from application.models import User, Files, Conversations, Messages
from flask import request, jsonify, send_from_directory
from application.database import db
from flask_jwt_extended import create_access_token
import os
import uuid
from datetime import datetime

UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


class UserAPI(Resource):
   # READ: Get a user by username
    def get(self, username=None):
        if username:
            user = User.query.get(username)
            if user:
                return user.as_dict(), 200
            return {"message": "User not found"}, 404
        else:
            # Get all users
            users = User.query.all()
            return [user.as_dict() for user in users], 200

   
    # UPDATE: Update an existing user
    def put(self, username):
        user = User.query.get(username)
        if not user:
            return {"message": "User not found"}, 404

        data = request.get_json()
        user.email = data.get("email", user.email)
        user.age = data.get("age", user.age)
        db.session.commit()
        return user.as_dict(), 200

    # DELETE: Remove a user
    def delete(self, username):
        user = User.query.get(username)
        if not user:
            return {"message": "User not found"}, 404
        
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted"}, 200




class LoginAPI(Resource):
    def post(self):
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return {"message": "Username and password required"}, 400

        user = User.query.get(username)
        if not user or not user.check_password(password):
            return {"message": "Invalid username or password"}, 401
        access_token = create_access_token(identity=username)

        return {
            "message": "Login successful",
            "access_token": access_token,
            "user": user.as_dict()
               }, 200



class RegisterAPI(Resource):
    def post(self):
        data = request.get_json()
        username = data.get("username")
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")
        age = data.get("age")
        
        # Validation
        if not username or not name or not email or not password:
            return {"message": "All fields are required"}, 400

        if User.query.get(username):
            return {"message": "Username already exists"}, 400

        # Create user
        new_user = User(
            username=username,
            name=name,
            email=email,
            age=age
        )
        new_user.set_password(password)  # hash password

        db.session.add(new_user)
        db.session.commit()

        return {"message": "User created successfully", "user": new_user.as_dict()}, 201


class FileAPI(Resource):
    # Upload a file
    def post(self):
        if 'file' not in request.files:
            return {"message": "No file part in the request"}, 400

        file = request.files['file']
        user_id = request.form.get("user_id")
        conversation_id = request.form.get("conversation_id")

        if not file or file.filename == '':
            return {"message": "No file selected"}, 400

        if not user_id or not conversation_id:
            return {"message": "User ID and Conversation ID are required"}, 400

        # Generate a unique file ID and save the file
        file_id = str(uuid.uuid4())
        filename = f"{file_id}_{file.filename}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # Save file metadata to the database
        new_file = Files(
            file_id=file_id,
            user_id=user_id,
            conversation_id=conversation_id,
            filename=file.filename,
            filepath=filepath,
            upload_date=datetime.utcnow()
        )
        db.session.add(new_file)
        db.session.commit()

        return {"message": "File uploaded successfully", "file": new_file.as_dict()}, 201

    # Get file metadata
    def get(self, file_id=None):
        if file_id:
            file = Files.query.get(file_id)
            if not file:
                return {"message": "File not found"}, 404
            return file.as_dict(), 200
        else:
            files = Files.query.all()
            return [file.as_dict() for file in files], 200

    # Download a file
    def post(self, file_id):
        file = Files.query.get(file_id)
        if not file:
            return {"message": "File not found"}, 404

        directory = os.path.dirname(file.filepath)
        filename = os.path.basename(file.filepath)
        return send_from_directory(directory, filename, as_attachment=True)

    # Delete a file
    def delete(self, file_id):
        file = Files.query.get(file_id)
        if not file:
            return {"message": "File not found"}, 404

        # Delete the file from the filesystem
        if os.path.exists(file.filepath):
            os.remove(file.filepath)

        # Delete the file record from the database
        db.session.delete(file)
        db.session.commit()

        return {"message": "File deleted successfully"}, 200



class AIServiceAPI(Resource):
    def post(self):
        data = request.get_json()
        user_input = data.get("user_input")

        if not user_input:
            return {"message": "User input is required"}, 400

        from application.ai_agent import model_agent

        response = model_agent.run(user_input=user_input)

        return {"response": response}, 200


class ConversationsAPI(Resource):
    # Get all conversations for a specific user or a specific conversation
    def get(self, conversation_id=None, user_id=None):
        if user_id:
            # Get all conversations for a specific user
            conversations = Conversations.query.filter_by(user_id=user_id).all()
            if not conversations:
                return {"message": "No conversations found for the user"}, 404

            # Include messages for each conversation
            result = []
            for conversation in conversations:
                result.append(conversation.as_dict())
            return result, 200

        elif conversation_id:
            # Get a specific conversation by ID
            conversation = Conversations.query.get(conversation_id)
            if not conversation:
                return {"message": "Conversation not found"}, 404

            return conversation.as_dict(), 200

        else:
            # Get all conversations
            conversations = Conversations.query.all()
            return [conversation.as_dict() for conversation in conversations], 200

    # Create a new conversation
    def post(self):
        data = request.get_json()
        user_id = data.get("user_id")
        title = data.get("title")
        messages = data.get("messages", [])  # List of messages

        if not user_id or not title:
            return {"message": "User ID and title are required"}, 400

        # Generate a unique conversation ID
        conversation_id = str(uuid.uuid4())

        # Create a new conversation
        new_conversation = Conversations(
            conversation_id=conversation_id,
            user_id=user_id,
            title=title
        )
        db.session.add(new_conversation)

        # Add messages to the conversation
        for msg in messages:
            new_message = Messages(
                message_id=str(uuid.uuid4()),
                conversation_id=conversation_id,
                sender=msg.get("sender"),
                message=msg.get("message"),
                timestamp=datetime.utcnow()
            )
            db.session.add(new_message)

        db.session.commit()

        return {"message": "Conversation created successfully", "conversation": new_conversation.as_dict()}, 201

    # Update an existing conversation
    def put(self, conversation_id):
        conversation = Conversations.query.get(conversation_id)
        if not conversation:
            return {"message": "Conversation not found"}, 404

        data = request.get_json()
        conversation.title = data.get("title", conversation.title)
        db.session.commit()

        return {"message": "Conversation updated successfully", "conversation": conversation.as_dict()}, 200

    # Delete a conversation
    def delete(self, conversation_id):
        conversation = Conversations.query.get(conversation_id)
        if not conversation:
            return {"message": "Conversation not found"}, 404

        # Delete all messages associated with the conversation
        Messages.query.filter_by(conversation_id=conversation_id).delete()

        # Delete the conversation
        db.session.delete(conversation)
        db.session.commit()

        return {"message": "Conversation deleted successfully"}, 200


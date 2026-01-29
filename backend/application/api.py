from flask_restful import Resource 
from application.models import User
from flask import request 
from application.database import db
from flask_jwt_extended import create_access_token

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



    
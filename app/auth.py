from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
import os

# Create a blueprint for auth
auth = Blueprint('auth', __name__)

# MongoDB setup
client = MongoClient(os.environ.get('MONGO_URI'))
db = client.get_database('bookstore_db')
users = db.users

@auth.route('/register', methods=['POST'])
def register():
    # Get user data from request
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    if not email or not password:
        return jsonify({"msg": "Missing email or password"}), 400

    # Check if user already exists
    if users.find_one({"email": email}):
        return jsonify({"msg": "User already exists"}), 409

    # Hash the password
    hashed_password = generate_password_hash(password)

    # Create new user
    user = {
        "email": email,
        "password": hashed_password
    }
    users.insert_one(user)

    return jsonify({"msg": "User registered successfully"}), 201

@auth.route('/login', methods=['POST'])
def login():
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    if not email or not password:
        return jsonify({"msg": "Missing email or password"}), 400

    # Find user in database
    user = users.find_one({"email": email})
    if user and check_password_hash(user['password'], password):
        # Create JWTs
        access_token = create_access_token(identity=email)
        refresh_token = create_refresh_token(identity=email)
        return jsonify(access_token=access_token, refresh_token=refresh_token), 200
    else:
        return jsonify({"msg": "Bad username or password"}), 401

@auth.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    # Generate new access token
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    return jsonify(access_token=new_access_token), 200

@auth.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
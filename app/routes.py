from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Book, Order, Review

api = Blueprint('api', __name__)

@api.route('/users/register', methods=['POST'])
def register_user():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({'error': 'Missing email or password'}), 400
    if User.find_user_by_email(email):
        return jsonify({'error': 'Email already exists'}), 409
    hashed_password = generate_password_hash(password)
    User.create_user(email, hashed_password)
    return jsonify({'message': 'User registered successfully'}), 201

@api.route('/users/login', methods=['POST'])
def login_user():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user = User.find_user_by_email(email)
    if user and check_password_hash(user['password'], password):
        access_token = create_access_token(identity=email)
        refresh_token = create_refresh_token(identity=email)
        return jsonify(access_token=access_token, refresh_token=refresh_token), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

@api.route('/users/logout', methods=['POST'])
@jwt_required()
def logout_user():
    # JWT Blacklisting
    return jsonify({'message': 'Successfully logged out'}), 200

@api.route('/users/profile', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def user_profile():
    if request.method == 'GET':
        current_user = get_jwt_identity()
        user = User.find_user_by_email(current_user)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        del user['password']  # Do not send the password hash back to the user
        return jsonify(user), 200
    elif request.method == 'PUT':
        current_user = get_jwt_identity()
        data = request.get_json()
        result = User.update_user(current_user, data)
        if result:
            return jsonify({'message': 'User profile updated'}), 200
        else:
            return jsonify({'error': 'Failed to update profile'}), 500
    elif request.method == 'DELETE':
        current_user = get_jwt_identity()
        result = User.delete_user(current_user)
        if result:
            return jsonify({'message': 'User deleted'}), 200
        else:
            return jsonify({'error': 'Failed to delete user'}), 500

# Book endpoints
@api.route('/books', methods=['GET'])
def get_books():
    books = Book.get_all_books()
    return jsonify({'books': books}), 200

@api.route('/books', methods=['POST'])
@jwt_required()
def add_book():
    data = request.get_json()
    result = Book.add_book(**data)
    if result:
        return jsonify({'message': 'Book added successfully'}), 201
    else:
        return jsonify({'error': 'Failed to add book'}), 500

@api.route('/books/<string:book_id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def handle_book(book_id):
    if request.method == 'GET':
        book = Book.find_book_by_id(book_id)
        if book:
            return jsonify(book), 200
        else:
            return jsonify({'error': 'Book not found'}), 404
    elif request.method == 'PUT':
        data = request.get_json()
        result = Book.update_book(book_id, data)
        if result:
            return jsonify({'message': 'Book updated successfully'}), 200
        else:
            return jsonify({'error': 'Failed to update book'}), 500
    elif request.method == 'DELETE':
        result = Book.delete_book(book_id)
        if result:
            return jsonify({'message': 'Book deleted successfully'}), 200
        else:
            return jsonify({'error': 'Failed to delete book'}), 500

# Order endpoints
@api.route('/orders', methods=['POST'])
@jwt_required()
def create_order():
    user_email = get_jwt_identity()
    data = request.get_json()
    result = Order.create_order(user_email, **data)
    if result:
        return jsonify({'message': 'Order created successfully'}), 201
    else:
        return jsonify({'error': 'Failed to create order'}), 500

@api.route('/orders/<string:order_id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def handle_order(order_id):
    if request.method == 'GET':
        order = Order.find_order_by_id(order_id)
        if order:
            return jsonify(order), 200
        else:
            return jsonify({'error': 'Order not found'}), 404
    elif request.method == 'PUT':
        data = request.get_json()
        result = Order.update_order(order_id, data)
        if result:
            return jsonify({'message': 'Order updated successfully'}), 200
        else:
            return jsonify({'error': 'Failed to update order'}), 500
    elif request.method == 'DELETE':
        result = Order.delete_order(order_id)
        if result:
            return jsonify({'message': 'Order canceled successfully'}), 200
        else:
            return jsonify({'error': 'Failed to cancel order'}), 500

@api.route('/reviews', methods=['POST'])
@jwt_required()
def add_review():
    data = request.get_json()
    result = Review.add_review(**data)
    if result:
        return jsonify({'message': 'Review added successfully'}), 201
    else:
        return jsonify({'error': 'Failed to add review'}), 500

@api.route('/reviews/<string:review_id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def handle_review(review_id):
    if request.method == 'GET':
        review = Review.find_review_by_id(review_id)
        if review:
            return jsonify(review), 200
        else:
            return jsonify({'error': 'Review not found'}), 404
    elif request.method == 'PUT':
        data = request.get_json()
        result = Review.update_review(review_id, data)
        if result:
            return jsonify({'message': 'Review updated successfully'}), 200
        else:
            return jsonify({'error': 'Failed to update review'}), 500
    elif request.method == 'DELETE':
        result = Review.delete_review(review_id)
        if result:
            return jsonify({'message': 'Review deleted successfully'}), 200
        else:
            return jsonify({'error': 'Failed to delete review'}), 500
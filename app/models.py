from pymongo import MongoClient
import os

# connect to MongoDB
client = MongoClient(os.environ.get('MONGO_URI'))
db = client['bookstore_db']

class User:
    collection = db['users']

    @staticmethod
    def create_user(email, password_hash):
        """Create a new user in the database."""
        return User.collection.insert_one({
            'email': email,
            'password': password_hash
        })

    @staticmethod
    def find_user_by_email(email):
        """Retrieve a user by email."""
        return User.collection.find_one({'email': email})

    @staticmethod
    def update_user(email, data):
        """Update user data."""
        return User.collection.update_one({'email': email}, {'$set': data})

    @staticmethod
    def delete_user(email):
        """Delete a user from the database."""
        return User.collection.delete_one({'email': email})

class Book:
    collection = db['books']

    @staticmethod
    def add_book(title, author, description, price):
        """Add a new book to the database."""
        return Book.collection.insert_one({
            'title': title,
            'author': author,
            'description': description,
            'price': price
        })

    @staticmethod
    def get_all_books():
        """Retrieve all books."""
        return list(Book.collection.find({}))

    @staticmethod
    def find_book_by_id(book_id):
        """Retrieve a book by its ID."""
        return Book.collection.find_one({'_id': book_id})

    @staticmethod
    def update_book(book_id, data):
        """Update book information."""
        return Book.collection.update_one({'_id': book_id}, {'$set': data})

    @staticmethod
    def delete_book(book_id):
        """Remove a book from the database."""
        return Book.collection.delete_one({'_id': book_id})

class Order:
    collection = db['orders']

    @staticmethod
    def create_order(user_email, books, status):
        """Create a new order."""
        return Order.collection.insert_one({
            'user_email': user_email,
            'books': books,
            'status': status
        })

    @staticmethod
    def get_orders_by_user_email(user_email):
        """Retrieve orders by user email."""
        return list(Order.collection.find({'user_email': user_email}))

    @staticmethod
    def update_order(order_id, data):
        """Update an order."""
        return Order.collection.update_one({'_id': order_id}, {'$set': data})

    @staticmethod
    def delete_order(order_id):
        """Delete an order."""
        return Order.collection.delete_one({'_id': order_id})
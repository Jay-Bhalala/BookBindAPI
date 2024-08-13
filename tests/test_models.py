import unittest
from app.models import User, Book, Order
from pymongo import MongoClient
import os

class TestModels(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Connect to the test database
        client = MongoClient(os.environ.get('MONGO_TEST_URI'))
        cls.db = client['test_bookstore']
        User.collection = cls.db['users']
        Book.collection = cls.db['books']
        Order.collection = cls.db['orders']

    def test_user_creation(self):
        User.create_user("test@example.com", "testpass")
        user = User.find_user_by_email("test@example.com")
        self.assertIsNotNone(user)
        self.assertEqual(user['email'], "test@example.com")

    def test_book_addition(self):
        Book.add_book("Test Book", "Author Name", "Description here", 9.99)
        book = Book.find_book_by_id("Test Book")
        self.assertIsNotNone(book)
        self.assertEqual(book['title'], "Test Book")

    def test_order_creation(self):
        Order.create_order("test@example.com", [{'book_id': 'book1', 'quantity': 1}], 'pending')
        order = Order.get_orders_by_user_email("test@example.com")[0]
        self.assertIsNotNone(order)
        self.assertEqual(order['status'], 'pending')

    @classmethod
    def tearDownClass(cls):
        # Clean up the database
        cls.db['users'].delete_many({})
        cls.db['books'].delete_many({})
        cls.db['orders'].delete_many({})
        client = MongoClient(os.environ.get('MONGO_TEST_URI'))
        client.drop_database('test_bookstore')

if __name__ == '__main__':
    unittest.main()
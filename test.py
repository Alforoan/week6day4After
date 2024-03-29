import sqlite3
import unittest
from advanced_user_operations import AdvancedUserOperations

class TestAdvancedUserOperations(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(':memory:')
        self.user_ops = AdvancedUserOperations()

        # Initialize the database schema
        self.user_ops.create_user_table()

    def tearDown(self):
        self.conn.close()

    def test_create_user_with_profile(self):
        self.user_ops.create_user_with_profile('Test User', 'test@example.com', 'password', age=30, gender='male', address='123 Test St')
        self.assertIsNotNone(self.user_ops.retrieve_user_by_email('test@example.com'))

    def test_update_user_profile(self):
        self.user_ops.create_user_with_profile('Test User', 'test@example.com', 'password', age=30, gender='male', address='123 Test St')
        self.user_ops.update_user_profile('test@example.com', age=35, address='456 Updated St')
        updated_user = self.user_ops.retrieve_user_by_email('test@example.com')
        self.assertEqual(updated_user[4], 35)  # Check if the age is updated
        self.assertEqual(updated_user[6], '456 Updated St')  # Check if the address is updated

    def test_delete_users_by_criteria(self):
        self.user_ops.create_user_with_profile('Test User 1', 'test1@example.com', 'password', age=30, gender='male', address='123 Test St')
        self.user_ops.create_user_with_profile('Test User 2', 'test2@example.com', 'password', age=40, gender='female', address='456 Test St')
        
        self.user_ops.delete_users_by_criteria(gender='female')

        remaining_users = self.user_ops.retrieve_users_by_criteria()
        self.assertEqual(len(remaining_users), 1)  # There should only be 1 user remaining

if __name__ == '__main__':
    unittest.main()

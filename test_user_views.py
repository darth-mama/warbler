import unittest
from app import app, db
from models import User


class UserViewsTestCase(unittest.TestCase):
    def setUp(self):
        """Set up test environment."""
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///warbler-test'
        app.config['TESTING'] = True
        self.client = app.test_client()

        with app.app_context():
            db.drop_all()
            db.create_all()

    def tearDown(self):
        """Clean up after tests."""
        with app.app_context():
            db.session.rollback()
            db.drop_all()

    def test_signup_route(self):
        """Test signup route."""
        response = self.client.post(
            '/signup', data={'username': 'testuser', 'email': 'test@example.com', 'password': 'password'}, follow_redirects=True)
        self.assertIn(b'Hello, testuser!', response.data)

    # Add more tests for other routes related to user views


if __name__ == '__main__':
    unittest.main()

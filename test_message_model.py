import unittest
from app import app, db
from models import User, Message


class MessageModelTestCase(unittest.TestCase):
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

    def test_message_repr(self):
        """Test __repr__ method of Message model."""
        user = User(username='testuser', email='test@example.com')
        db.session.add(user)
        db.session.commit()
        message = Message(text='Test message', user_id=user.id)
        db.session.add(message)
        db.session.commit()

        self.assertEqual(repr(message), '<Message testuser: Test message>')

    # Add more tests for other Message model methods


if __name__ == '__main__':
    unittest.main()

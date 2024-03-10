"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


from app import app
import os
from unittest import TestCase

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app


# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)

        # Test __repr__ method
        self.assertEqual(repr(u), f'<User #{u.id}: {u.username}, {u.email}>')

        # Test is_following and is_followed_by methods
        self.assertFalse(u.is_following(u))  # User is not following themselves
        # User is not followed by themselves
        self.assertFalse(u.is_followed_by(u))

        # Test follow method
        u2 = User(email="test2@test.com", username="testuser2",
                  password="HASHED_PASSWORD")
        db.session.add(u2)
        db.session.commit()
        u.following.append(u2)
        db.session.commit()
        self.assertTrue(u.is_following(u2))  # User is following u2
        self.assertTrue(u2.is_followed_by(u))  # u2 is followed by user

        # Test unfollow method
        u.unfollow(u2)
        db.session.commit()
        # User is not following u2 after unfollowing
        self.assertFalse(u.is_following(u2))

        # Test create method
        new_user = User.create(
            username="newuser", email="new@test.com", password="HASHED_PASSWORD")
        db.session.commit()
        # New user created successfully
        self.assertEqual(new_user.username, "newuser")

        # Test authenticate method
        authenticated_user = User.authenticate(
            username="testuser", password="HASHED_PASSWORD")
        # User authenticated successfully
        self.assertEqual(authenticated_user, u)

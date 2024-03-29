#!/usr/bin/env python3
"""
auth.py
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid


def _hash_password(password: str) -> bytes:
    """
    Hash a password with salt using bcrypt
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def _generate_uuid() -> str:
    """
    The function should return a string representation,
    of a new UUID. Use the uuid module.
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        add a new user and return the User object.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError("User {} already exists".format(email))
        except ValueError:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'),
                                            bcrypt.gensalt())
            user = self._db.add_user(email, hashed_password)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """
        Checking if the logins credentials are valid.
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('utf-8'),
                                  user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """
        Create a session for the user and return the session ID.
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            user.session_id = session_id
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        Get the corresponding user for a given session ID.
        """
        if session_id is None:
            return None

        try:
            return self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Destroy the session for the corresponding user.
        """
        try:
            user = self._db.find_user_by(id=user_id)
            user.session_id = None
            self._db.update_user(user.id, session_id=None)
        except NoResultFound:
            pass

    def get_reset_password_token(self, email: str) -> str:
        """
        Generate and return a reset password token for the user.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError(f"No user found with email: {email}")

        reset_token = str(uuid.uuid4())
        user.reset_token = reset_token
        self._db.update_user(user.id, reset_token=reset_token)

        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """Update user's password using the reset token."""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_password = _hash_password(password)
            user.hashed_password = hashed_password
            user.reset_token = None
            self._db.update_user(user.id,
                                 hashed_password=hashed_password,
                                 reset_token=None)
        except NoResultFound:
            raise ValueError("Invalid reset token")

#!/usr/bin/env python3
"""
auth.py
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """Hash a password with salt using bcrypt
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """
        initialize
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user and return the User object.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError("User {} already exists".format(email))
        except ValueError:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'),
                                            bcrypt.gensalt())
            user = self._db.add_user(email, hashed_password)
            return user

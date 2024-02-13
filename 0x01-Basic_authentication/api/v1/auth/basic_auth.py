#!/usr/bin/env python3
""" Module of basic_auth
"""
from .auth import Auth
import base64
from models.user import User
from typing import List, TypeVar


class BasicAuth(Auth):
    """
    class BasicAuth
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        returns the Base64 part of,
        the Authorization header for a Basic Authentication
        """
        if authorization_header is None or not isinstance(authorization_header,
                                                          str):
            return None

        if not authorization_header.startswith("Basic "):
            return None

        base64_credentials = authorization_header.split(" ", 1)[1]

        return base64_credentials

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """Decode the Base64 authorization header to UTF-8."""
        if (
            base64_authorization_header is None or
            not isinstance(base64_authorization_header, str)
        ):
            return None

        try:
            decoded_credentials = base64.b64decode(base64_authorization_header)
            decoded_credentials_utf8 = decoded_credentials.decode('utf-8')
            return decoded_credentials_utf8
        except Exception as e:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        returns the user email and password from the Base64 decoded value.
        """
        if (
            decoded_base64_authorization_header is None or
            not isinstance(decoded_base64_authorization_header, str) or
            ':' not in decoded_base64_authorization_header
        ):
            return None, None

        user_email, user_password = decoded_base64_authorization_header.split(
            ':', 1)
        return user_email, user_password

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """Return the User instance based on email and password."""
        if (
            user_email is None or not isinstance(user_email, str) or
            user_pwd is None or not isinstance(user_pwd, str)
        ):
            return None

        users = User.search({"email": user_email})
        if not users:
            return None

        user_instance = users[0]

        if not user_instance.is_valid_password(user_pwd):
            return None

        return user_instance

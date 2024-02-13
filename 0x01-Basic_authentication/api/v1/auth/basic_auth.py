#!/usr/bin/env python3
""" Module of basic_auth
"""
from .auth import Auth
import base64


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

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
        if authorization_header is None or not isinstance(authorization_header, str):
            return None

        if not authorization_header.startswith("Basic "):
            return None

        base64_credentials = authorization_header.split(" ", 1)[1]
        try:
            decoded_credentials = base64.b64decode(base64_credentials).decode('utf-8')
            return decoded_credentials
        except Exception as e:
            return None
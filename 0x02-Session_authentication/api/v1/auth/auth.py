#!/usr/bin/env python3
""" Module of auth
"""
from flask import request
from typing import List, TypeVar
import os


class Auth:
    """
    Auth class.
    """
    def __init__(self):
        """
        init
        """
        self.session_name = os.getenv('SESSION_NAME', '_my_session_id')

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        returns False - path
        """
        if path is None or not excluded_paths:
            return True

        path_with_slash = path if path.endswith("/") else path + "/"

        for excluded_path in excluded_paths:
            if "*" in excluded_path:
                prefix = excluded_path.rstrip("*")
                if path.startswith(prefix):
                    return False
            elif path_with_slash == excluded_path or path == excluded_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
         returns None - request
        """
        if request is not None:
            return request.headers.get('Authorization', None)
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        returns None - request
        """
        return None

    def session_cookie(self, request=None):
        """
        session cookie
        """
        if request is not None:
            return request.cookies.get(self.session_name, None)
        return None

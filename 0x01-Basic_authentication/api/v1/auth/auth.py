#!/usr/bin/env python3
""" Module of auth
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """
    Auth class.
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        returns False - path
        """
        if path is None or not excluded_paths:
            return True
        path_with_slash = path if path.endswith("/") else path + "/"
        return path_with_slash not in excluded_paths

    def authorization_header(self, request=None) -> str:
        """
         returns None - request
        """
        if request is not None:
            return request.headers.get('Authorisation', None)
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        returns None - request
        """
        return None

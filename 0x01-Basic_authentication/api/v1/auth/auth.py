#!/usr/bin/env python3
""" Module of auth
"""
from flask import request
from api.v1.views import app_views
from typing import List, TypeVar


class Auth:
    """
    Auth class.
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        returns False - path
        """
        return path not in excluded_paths

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

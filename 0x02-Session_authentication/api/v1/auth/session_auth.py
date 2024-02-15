#!/usr/bin/env python3
"""
class session_auth
"""
from api.v1.auth.auth import Auth
from models.user import User
import uuid



class SessionAuth(Auth):
    """
    class session auth
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
         creates a Session ID for a user_id.
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        returns a User ID based on a Session ID.
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id, None)

    def current_user(self, request=None) -> User:
        """
        returns a User instance based on a cookie value.
        """
        if request is None:
            return None

        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)

        if user_id:
            return User.get(user_id)

        return None

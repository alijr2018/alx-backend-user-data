#!/usr/bin/env python3
"""
New view for Session Authentication
"""
from flask import Flask, request, jsonify, make_response
from api.v1.views import app_views
from api.v1.auth.session_auth import SessionAuth
from models.user import User
import os

auth = SessionAuth()
app = Flask(__name__)


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def auth_session_login():
    """
    Handles user authentication for session
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    user = User.search({"email": email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404

    if not user[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    session_id = auth.create_session(user[0].id)
    user_json = user[0].to_json()
    response = make_response(jsonify(user_json), 200)
    response.set_cookie(os.getenv("SESSION_NAME", "_my_session_id"),
                        session_id)

    return response

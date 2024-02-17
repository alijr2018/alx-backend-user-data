#!/usr/bin/env python3
""" Session Authentication view module
"""
from flask import Flask, request, jsonify
from api.v1.app import auth
from models.user import User

app = Flask(__name__)


@app.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_auth_login():
    """ Session authentication login route
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    user = User.search({'email': email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404
    if not user[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    session_id = auth.create_session(user[0].id)
    response = jsonify(user[0].to_json())
    response.set_cookie(auth.session_name, session_id)
    return response

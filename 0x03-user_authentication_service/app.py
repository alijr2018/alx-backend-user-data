#!/usr/bin/env python3
"""
app.py
"""
from flask import Flask, request, jsonify, abort, redirect

from flask.json import JSONEncoder

from auth import Auth

app = Flask(__name__)
app.url_map.strict_slashes = False
app.json_encoder = JSONEncoder
AUTH = Auth()


@app.route("/")
def welcome() -> str:
    """
    Welcome
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> str:
    """
    register user
    """
    try:
        email = request.form.get('email')
        password = request.form.get('password')

        user = AUTH.register_user(email, password)

        return jsonify({"email": user.email, "message": "user created"})
    except ValueError as e:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login() -> str:
    """
    Login endpoint for creating a session.
    """
    if 'email' not in request.form or 'password' not in request.form:
        abort(400)

    email = request.form['email']
    password = request.form['password']

    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie('session_id', session_id)
        return response
    else:
        abort(401)


@app.route('/sessions', methods=['DELETE'])
def logout() -> str:
    """
    Logout route to destroy the session and redirect to home.
    """
    session_id = request.cookies.get('session_id')

    if not session_id:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)

    if not user:
        abort(403)

    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route('/profile', methods=['GET'])
def profile() -> str:
    """
    Profile route to retrieve user information.
    """
    session_id = request.cookies.get('session_id')

    if not session_id:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)

    if not user:
        abort(403)

    return jsonify({"email": user.email}), 200


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token() -> str:
    """
    Generate and return a reset password token.
    """
    if request.method == 'POST':
        email = request.form.get('email')
        try:
            reset_token = AUTH.get_reset_password_token(email)
            return jsonify({"email": email, "reset_token": reset_token}), 200
        except ValueError:
            abort(403)
    else:
        abort(405)


@app.route('/reset_password', methods=['PUT'])
def update_password() -> str:
    """Update user password using reset token."""
    try:
        email = request.form['email']
        reset_token = request.form['reset_token']
        new_password = request.form['new_password']

        AUTH.update_password(reset_token, new_password)

        return jsonify({
            "email": email,
            "message": "Password updated"
        }), 200

    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

#!/usr/bin/env python3
"""
encrypt_password.py
"""
import bcrypt


def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

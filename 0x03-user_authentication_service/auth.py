#!/usr/bin/env python3
"""
auth.py
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """
    Hash a password with salt using bcrypt
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

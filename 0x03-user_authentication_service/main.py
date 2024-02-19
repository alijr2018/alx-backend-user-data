#!/usr/bin/env python3
"""
Main file, 0. User model
"""
from user import User
from db import DB

print(User.__tablename__)

for column in User.__table__.columns:
    print("{}: {}".format(column, column.type))


"""
Main file, 1. create user
"""


my_db = DB()

user_1 = my_db.add_user("test@test.com", "SuperHashedPwd")
print(user_1.id)

user_2 = my_db.add_user("test1@test.com", "SuperHashedPwd1")
print(user_2.id)

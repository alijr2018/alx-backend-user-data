#!/usr/bin/env python3
"""filtered_logger.py"""
import re
import logging
from typing import List
import csv
import os
from mysql.connector import MySQLConnection
import mysql.connector


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Return value from log records
        """
        log_message = super().format(record)
        return filter_datum(self.fields,
                            self.REDACTION, log_message, self.SEPARATOR)


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """The function use a regex to replace occurrences field values."""
    return re.sub(fr'(\b(?:{"|".join(fields)})=)[^{separator}]+',
                  fr'\1{redaction}', message)


PII_FIELDS = ("name", "email", "phone", "ssn", "credit_card")


def get_logger() -> logging.Logger:
    """ Returns a logging.Logger object """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    target_handler = logging.StreamHandler()
    target_handler.setLevel(logging.INFO)

    formatter = RedactingFormatter(list(PII_FIELDS))
    target_handle.setFormatter(formatter)

    logger.addHandler(target_handler)
    return logger


def get_db() -> MySQLConnection:
    """
    get_db
    """
    username = os.environ.get('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.environ.get('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.environ.get('PERSONAL_DATA_DB_HOST', 'localhost')
    database = os.environ.get('PERSONAL_DATA_DB_NAME')

    db = mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=database
    )

    return db

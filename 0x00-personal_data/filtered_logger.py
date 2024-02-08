#!/usr/bin/env python3
"""filtered_logger.py"""
import re
import logging
from typing import List


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


def get_logger():
    """
    function that takes no arguments and returns a logging.Logger object.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    return logger

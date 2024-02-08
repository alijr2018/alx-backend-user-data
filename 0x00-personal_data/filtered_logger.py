#!/usr/bin/env python3
"""filtered_logger.py"""
import re
import logging


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        NotImplementedError
        log_message = super().format(record)
        return filter_datum(self.fields,
                            self.REDACTION, log_message, self.SEPARATOR)


def filter_datum(fields, redaction, message, separator):
    """The function use a regex to replace occurrences field values."""
    return re.sub(fr'(\b(?:{"|".join(fields)})=)[^{separator}]+',
                  fr'\1{redaction}', message)

#!/usr/bin/env python3
"""
filtered_logger.py
"""
import re


def filter_datum(fields, redaction, message, separator):
    pattern = re.compile(
        r'(?<=' + separator + '|'.join(fields) + '=' + ')[^' + separator + ']*'
    )
    return pattern.sub(redaction, message)

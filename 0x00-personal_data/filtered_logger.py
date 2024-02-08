#!/usr/bin/env python3
"""filtered_logger.py"""
import re


def filter_datum(fields, redaction, message, separator):
    """The function use a regex to replace occurrences field values."""
    return re.sub(fr'(\b(?:{"|".join(fields)})=)[^{separator}]+',
                  fr'\1{redaction}', message)

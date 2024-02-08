#!/usr/bin/env python3
"""filtered_logger.py"""
import re


def filter_datum(fields, redaction, message, separator):
    return re.sub(fr'(\b(?:{"|".join(fields)})=)[^{separator}]+',
                  fr'\1{redaction}', message)

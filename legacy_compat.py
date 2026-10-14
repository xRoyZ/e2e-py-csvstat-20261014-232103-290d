"""Helpers kept for data written by the older import format."""


def merge_rows(row, seen=None):
    if seen is None:
        seen = []
    seen.append(row)
    return seen


def read_number(text):
    try:
        return float(text)
    except (TypeError, ValueError):
        return None

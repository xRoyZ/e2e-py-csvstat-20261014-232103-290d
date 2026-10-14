"""Tests für die Spaltenauswahl ``select.select_columns``."""

import pytest

from csvstat import errors
from csvstat.select import select_columns


def test_none_returns_all_columns_in_file_order() -> None:
    headers = ["a", "b", "c"]

    assert select_columns(headers, None) == [0, 1, 2]


def test_none_with_empty_headers_returns_empty() -> None:
    assert select_columns([], None) == []


def test_requested_order_is_preserved() -> None:
    headers = ["a", "b", "c"]

    assert select_columns(headers, "b,a") == [1, 0]


def test_single_column() -> None:
    headers = ["a", "b", "c"]

    assert select_columns(headers, "c") == [2]


def test_surrounding_whitespace_is_trimmed() -> None:
    headers = ["a", "b", "c"]

    assert select_columns(headers, " b , a ") == [1, 0]


def test_duplicate_names_are_kept_in_order() -> None:
    headers = ["a", "b"]

    assert select_columns(headers, "b,b,a") == [1, 1, 0]


def test_unknown_name_raises_column_error() -> None:
    headers = ["a", "b"]

    with pytest.raises(errors.ColumnError) as excinfo:
        select_columns(headers, "zzz")

    assert excinfo.value.name == "zzz"


def test_unknown_name_message_names_the_column() -> None:
    with pytest.raises(errors.ColumnError) as excinfo:
        select_columns(["a", "b"], "b,zzz")

    assert "zzz" in str(excinfo.value)

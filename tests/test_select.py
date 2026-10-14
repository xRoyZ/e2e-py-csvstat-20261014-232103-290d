"""Tests für die Spaltenauswahl in :mod:`csvstat.select`."""

import pytest

from csvstat import errors, select


def test_none_returns_all_columns_in_file_order() -> None:
    headers = ["a", "b", "c"]
    assert select.select_columns(headers, None) == [0, 1, 2]


def test_requested_order_is_preserved() -> None:
    headers = ["a", "b", "c"]
    assert select.select_columns(headers, "b,a") == [1, 0]


def test_surrounding_whitespace_is_trimmed() -> None:
    headers = ["a", "b", "c"]
    assert select.select_columns(headers, " b , a ") == [1, 0]


def test_single_column() -> None:
    headers = ["a", "b"]
    assert select.select_columns(headers, "a") == [0]


def test_unknown_name_raises_column_error() -> None:
    headers = ["a", "b"]
    with pytest.raises(errors.ColumnError) as excinfo:
        select.select_columns(headers, "zzz")
    assert excinfo.value.name == "zzz"


def test_unknown_name_message_names_column() -> None:
    headers = ["a", "b"]
    with pytest.raises(errors.ColumnError) as excinfo:
        select.select_columns(headers, "a,zzz")
    assert "zzz" in str(excinfo.value)

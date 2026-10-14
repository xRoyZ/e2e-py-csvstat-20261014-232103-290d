"""Tests für die Berechnung der Spaltenstatistiken."""

import pytest

from csvstat.reading import Table
from csvstat.stats import ColumnStats, compute_stats


def test_numeric_column_reports_min_max_mean_and_missing() -> None:
    table = Table(headers=["wert"], rows=[["2"], ["4"], [""], ["6"]])

    stats = compute_stats(table, [0])

    assert stats == [
        ColumnStats(
            name="wert",
            kind="numeric",
            count=3,
            missing=1,
            minimum=2.0,
            maximum=6.0,
            mean=4.0,
            unique=None,
        )
    ]


def test_whitespace_only_counts_as_missing() -> None:
    table = Table(headers=["wert"], rows=[["1"], ["   "], ["3"]])

    stats = compute_stats(table, [0])

    assert stats[0].missing == 1
    assert stats[0].count == 2
    assert stats[0].mean == 2.0


def test_column_with_non_numeric_value_is_text() -> None:
    table = Table(headers=["wert"], rows=[["1"], ["zwei"], ["3"]])

    stats = compute_stats(table, [0])

    assert stats[0].kind == "text"
    assert stats[0].minimum is None
    assert stats[0].maximum is None
    assert stats[0].mean is None


def test_text_column_counts_unique_without_missing() -> None:
    table = Table(headers=["farbe"], rows=[["rot"], ["blau"], ["rot"], [""]])

    stats = compute_stats(table, [0])

    assert stats[0].kind == "text"
    assert stats[0].count == 3
    assert stats[0].missing == 1
    assert stats[0].unique == 2


def test_mean_is_rounded_to_four_decimals() -> None:
    table = Table(headers=["wert"], rows=[["1"], ["1"], ["2"]])

    stats = compute_stats(table, [0])

    assert stats[0].mean == pytest.approx(1.3333)


def test_float_values_are_numeric() -> None:
    table = Table(headers=["wert"], rows=[["1.5"], ["2"], ["3.25"]])

    stats = compute_stats(table, [0])

    assert stats[0].kind == "numeric"
    assert stats[0].minimum == pytest.approx(1.5)
    assert stats[0].maximum == pytest.approx(3.25)


def test_header_only_file_yields_zero_counts() -> None:
    table = Table(headers=["zahl", "wort"], rows=[])

    stats = compute_stats(table, [0, 1])

    assert stats[0].count == 0
    assert stats[0].missing == 0
    assert stats[0].unique == 0
    assert stats[1].count == 0
    assert stats[1].missing == 0
    assert stats[1].unique == 0


def test_all_missing_column_has_zero_unique() -> None:
    table = Table(headers=["wert"], rows=[[""], ["   "]])

    stats = compute_stats(table, [0])

    assert stats[0].kind == "text"
    assert stats[0].count == 0
    assert stats[0].missing == 2
    assert stats[0].unique == 0


def test_indices_order_is_preserved() -> None:
    table = Table(headers=["a", "b", "c"], rows=[["1", "x", "2"]])

    stats = compute_stats(table, [2, 0])

    assert [column.name for column in stats] == ["c", "a"]

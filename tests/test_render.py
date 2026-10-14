"""Tests für den deutschen Textbericht."""

from pathlib import Path

from csvstat.reading import read_csv
from csvstat.render import render_text
from csvstat.stats import ColumnStats, compute_stats


def numeric(name: str = "wert") -> ColumnStats:
    return ColumnStats(
        name=name,
        kind="numeric",
        count=3,
        missing=1,
        minimum=1.0,
        maximum=3.0,
        mean=2.0,
        unique=None,
    )


def text(name: str = "farbe") -> ColumnStats:
    return ColumnStats(
        name=name,
        kind="text",
        count=2,
        missing=0,
        minimum=None,
        maximum=None,
        mean=None,
        unique=2,
    )


def test_report_is_deterministic() -> None:
    stats = [numeric(), text()]

    first = render_text("data.csv", stats)
    second = render_text("data.csv", stats)

    assert first == second


def test_report_contains_numeric_values_with_four_decimals() -> None:
    report = render_text("data.csv", [numeric()])

    assert "Anzahl: 3" in report
    assert "Fehlend: 1" in report
    assert "Minimum: 1.0000" in report
    assert "Maximum: 3.0000" in report
    assert "Mittelwert: 2.0000" in report


def test_report_contains_unique_for_text_column() -> None:
    report = render_text("data.csv", [text()])

    assert "Eindeutig: 2" in report
    assert "Mittelwert" not in report


def test_columns_follow_given_order() -> None:
    report = render_text("data.csv", [text("zweite"), numeric("erste")])

    assert report.index("zweite") < report.index("erste")


def test_column_names_are_sanitized() -> None:
    report = render_text("data.csv", [text("wert\x1b[31m")])

    assert "\x1b" not in report
    assert "wert[31m" in report


def test_file_name_is_sanitized() -> None:
    report = render_text("da\x1btei.csv", [])

    assert "\x1b" not in report
    assert "Datei: datei.csv" in report


def test_empty_stats_render_without_error() -> None:
    report = render_text("leer.csv", [])

    assert report == "Datei: leer.csv"


def test_reading_stats_and_text_report_work_together(tmp_path: Path) -> None:
    target = tmp_path / "daten.csv"
    target.write_text("name,alter\nAnna,31\nBen,\n", encoding="utf-8")

    table = read_csv(str(target), ",")
    column_stats = compute_stats(table, list(range(len(table.headers))))
    report = render_text(str(target), column_stats)

    assert "Spalte: name" in report
    assert "Spalte: alter" in report
    assert "Anzahl: 1" in report
    assert "Fehlend: 1" in report
    assert "Mittelwert: 31.0000" in report

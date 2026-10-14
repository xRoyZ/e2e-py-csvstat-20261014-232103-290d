"""Tests für die JSON-Ausgabe der Spaltenstatistiken."""

import json
from pathlib import Path

from csvstat.reading import read_csv
from csvstat.render_json import render_json
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


def test_output_is_valid_single_json_object() -> None:
    raw = render_json("data.csv", [numeric(), text()])

    parsed = json.loads(raw)

    assert isinstance(parsed, dict)
    assert set(parsed) == {"file", "columns"}


def test_json_loads_accepts_output() -> None:
    raw = render_json("data.csv", [numeric()])

    parsed = json.loads(raw)

    assert parsed["file"] == "data.csv"
    assert len(parsed["columns"]) == 1


def test_numeric_column_keys_and_values() -> None:
    column = json.loads(render_json("data.csv", [numeric()]))["columns"][0]

    assert set(column) == {
        "name",
        "type",
        "count",
        "missing",
        "min",
        "max",
        "mean",
        "unique",
    }
    assert column["name"] == "wert"
    assert column["type"] == "numeric"
    assert column["count"] == 3
    assert column["missing"] == 1
    assert column["min"] == 1.0
    assert column["max"] == 3.0
    assert column["mean"] == 2.0
    assert column["unique"] is None


def test_text_column_keys_and_values() -> None:
    column = json.loads(render_json("data.csv", [text()]))["columns"][0]

    assert column["type"] == "text"
    assert column["count"] == 2
    assert column["missing"] == 0
    assert column["unique"] == 2
    assert column["min"] is None
    assert column["max"] is None
    assert column["mean"] is None


def test_numbers_are_json_numbers_not_strings() -> None:
    column = json.loads(render_json("data.csv", [numeric()]))["columns"][0]

    assert isinstance(column["min"], (int, float))
    assert isinstance(column["mean"], float)
    assert isinstance(column["count"], int)
    assert isinstance(column["unique"], type(None))


def test_output_is_deterministic() -> None:
    stats = [numeric(), text()]

    first = render_json("data.csv", stats)
    second = render_json("data.csv", stats)

    assert first == second


def test_columns_follow_given_order() -> None:
    parsed = json.loads(render_json("data.csv", [text("zweite"), numeric("erste")]))

    names = [column["name"] for column in parsed["columns"]]

    assert names == ["zweite", "erste"]


def test_column_names_are_sanitized() -> None:
    column = json.loads(render_json("data.csv", [text("wert\x1b[31m")]))["columns"][0]

    assert "\x1b" not in column["name"]
    assert column["name"] == "wert[31m"


def test_file_name_is_sanitized() -> None:
    parsed = json.loads(render_json("da\x1btei.csv", []))

    assert parsed["file"] == "datei.csv"
    assert parsed["columns"] == []


def test_reading_stats_and_json_render_work_together(tmp_path: Path) -> None:
    target = tmp_path / "daten.csv"
    target.write_text("name,alter\nAnna,31\nBen,\n", encoding="utf-8")

    table = read_csv(str(target), ",")
    column_stats = compute_stats(table, list(range(len(table.headers))))
    parsed = json.loads(render_json(str(target), column_stats))

    assert [column["name"] for column in parsed["columns"]] == ["name", "alter"]
    assert parsed["columns"][0]["type"] == "text"
    assert parsed["columns"][1]["type"] == "numeric"
    assert parsed["columns"][1]["mean"] == 31.0

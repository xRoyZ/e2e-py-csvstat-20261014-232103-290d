"""Tests für das Einlesen von CSV-Dateien."""

from pathlib import Path

import pytest

from csvstat import errors
from csvstat.reading import read_csv


def write_csv(tmp_path: Path, content: str, name: str = "data.csv") -> str:
    target = tmp_path / name
    target.write_text(content, encoding="utf-8")
    return str(target)


def test_reads_header_and_rows(tmp_path: Path) -> None:
    path = write_csv(tmp_path, "name,alter\nAnna,31\nBen,25\n")

    table = read_csv(path, ",")

    assert table.headers == ["name", "alter"]
    assert table.rows == [["Anna", "31"], ["Ben", "25"]]


def test_header_only_file_is_valid(tmp_path: Path) -> None:
    path = write_csv(tmp_path, "name,alter\n")

    table = read_csv(path, ",")

    assert table.headers == ["name", "alter"]
    assert table.rows == []


def test_uses_given_delimiter(tmp_path: Path) -> None:
    path = write_csv(tmp_path, "name;alter\nAnna;31\n")

    table = read_csv(path, ";")

    assert table.headers == ["name", "alter"]
    assert table.rows == [["Anna", "31"]]


def test_tab_delimiter(tmp_path: Path) -> None:
    path = write_csv(tmp_path, "name\talter\nAnna\t31\n")

    table = read_csv(path, "\t")

    assert table.headers == ["name", "alter"]


def test_bom_is_stripped_from_first_header(tmp_path: Path) -> None:
    target = tmp_path / "bom.csv"
    target.write_bytes(b"\xef\xbb\xbfname,alter\nAnna,31\n")

    table = read_csv(str(target), ",")

    assert table.headers == ["name", "alter"]


def test_missing_file_raises_input_error(tmp_path: Path) -> None:
    with pytest.raises(errors.InputError):
        read_csv(str(tmp_path / "fehlt.csv"), ",")


def test_empty_file_raises_input_error(tmp_path: Path) -> None:
    path = write_csv(tmp_path, "")

    with pytest.raises(errors.InputError):
        read_csv(path, ",")


def test_directory_raises_input_error(tmp_path: Path) -> None:
    with pytest.raises(errors.InputError):
        read_csv(str(tmp_path), ",")


def test_wrong_field_count_raises_parse_error_with_line_number(tmp_path: Path) -> None:
    path = write_csv(tmp_path, "name,alter\nAnna,31\nBen,25,extra\n")

    with pytest.raises(errors.ParseError) as excinfo:
        read_csv(path, ",")

    assert excinfo.value.line == 3
    assert "3" in str(excinfo.value)
    assert "2" in str(excinfo.value)

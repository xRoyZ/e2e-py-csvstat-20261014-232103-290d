"""Kommandozeilen-Einstiegspunkt von csvstat."""

import argparse
import sys

from csvstat import errors, reading, render, render_json, select, stats


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="csvstat",
        description="Berechnet Spaltenstatistiken für eine CSV-Datei.",
    )
    parser.add_argument("datei", help="Pfad zur einzulesenden CSV-Datei.")
    parser.add_argument(
        "--delimiter",
        default=",",
        metavar="ZEICHEN",
        help=(
            "Trennzeichen der CSV-Datei (Standard: ','). "
            "Die Folge \\t steht für ein Tabulatorzeichen."
        ),
    )
    parser.add_argument(
        "--columns",
        default=None,
        metavar="A,B",
        help=(
            "Kommagetrennte Liste von Spaltennamen; gibt nur diese Spalten "
            "in der angegebenen Reihenfolge aus."
        ),
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="as_json",
        help="Gibt das Ergebnis als JSON-Objekt statt als Textbericht aus.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Führt die CLI aus und liefert den Exit-Code zurück."""
    parser = _build_parser()
    args = parser.parse_args(argv)

    delimiter = args.delimiter
    if delimiter == "\\t":
        delimiter = "\t"

    try:
        table = reading.read_csv(args.datei, delimiter)
        indices = select.select_columns(table.headers, args.columns)
        column_stats = stats.compute_stats(table, indices)
        if args.as_json:
            output = render_json.render_json(args.datei, column_stats)
        else:
            output = render.render_text(args.datei, column_stats)
    except errors.CsvstatError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    print(output)
    return 0

"""Lesen einer CSV-Datei in eine :class:`Table`."""

import csv
from dataclasses import dataclass

from csvstat import errors


@dataclass
class Table:
    """Kopfzeile und Datenzeilen einer CSV-Datei."""

    headers: list[str]
    rows: list[list[str]]


def _read_rows(path: str, delimiter: str) -> tuple[list[str], list[list[str]]]:
    """Liest Kopfzeile und Datenzeilen aus einer geöffneten CSV-Datei."""
    with open(path, encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle, delimiter=delimiter)
        try:
            headers = next(reader)
        except StopIteration:
            raise errors.InputError(f"Die Datei '{path}' ist leer.") from None

        rows: list[list[str]] = []
        for line_number, row in enumerate(reader, start=2):
            if len(row) != len(headers):
                raise errors.ParseError(
                    line_number,
                    (f"Zeile {line_number} hat {len(row)} Felder, erwartet werden {len(headers)}."),
                )
            rows.append(row)
    return headers, rows


def read_csv(path: str, delimiter: str) -> Table:
    """Liest die CSV-Datei unter ``path`` mit ``delimiter``.

    Das Encoding ist ``utf-8-sig``, sodass ein vorhandener BOM entfernt wird und
    den ersten Spaltennamen nicht verfälscht. Die erste Zeile ist die Kopfzeile.
    Eine fehlende, nicht lesbare oder leere Datei führt zu :class:`InputError`,
    eine Datenzeile mit abweichender Feldanzahl zu :class:`ParseError` (mit der
    1-basierten Zeilennummer der betroffenen Zeile).
    """
    try:
        headers, rows = _read_rows(path, delimiter)
    except FileNotFoundError:
        raise errors.InputError(f"Die Datei '{path}' wurde nicht gefunden.") from None
    except IsADirectoryError:
        raise errors.InputError(f"'{path}' ist keine Datei.") from None
    except PermissionError:
        raise errors.InputError(f"Die Datei '{path}' ist nicht lesbar.") from None
    except OSError:
        raise errors.InputError(f"Die Datei '{path}' konnte nicht geöffnet werden.") from None

    return Table(headers=headers, rows=rows)

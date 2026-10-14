"""JSON-Ausgabe der Spaltenstatistiken.

Die JSON-Schlüssel sind englisch; die Ausgabe ist genau ein JSON-Objekt, das
``json.loads`` akzeptiert. Spaltennamen und der Dateipfad durchlaufen
:func:`csvstat.sanitize.sanitize`.
"""

import json

from csvstat.sanitize import sanitize
from csvstat.stats import ColumnStats

__all__ = ["render_json", "sanitize"]


def _column_object(column: ColumnStats) -> dict[str, object]:
    """Baut das JSON-taugliche Wörterbuch genau einer Spalte."""
    return {
        "name": sanitize(column.name),
        "type": sanitize(column.kind),
        "count": column.count,
        "missing": column.missing,
        "min": column.minimum,
        "max": column.maximum,
        "mean": column.mean,
        "unique": column.unique,
    }


def render_json(path: str, stats: list[ColumnStats]) -> str:
    """Rendert ``stats`` als ein JSON-Objekt für die Datei ``path``.

    Die Ausgabe ist deterministisch: Spalten erscheinen in der Reihenfolge von
    ``stats``, Zahlen sind JSON-Zahlen und nicht anwendbare Schlüssel sind
    ``null``. Spaltennamen und der Dateipfad durchlaufen
    :func:`csvstat.sanitize.sanitize`.
    """
    payload = {
        "file": sanitize(path),
        "columns": [_column_object(column) for column in stats],
    }
    return json.dumps(payload)

"""Berechnung von Spaltenstatistiken."""

from dataclasses import dataclass

from csvstat.reading import Table


@dataclass
class ColumnStats:
    """Statistik einer einzelnen Spalte.

    ``kind`` ist exakt ``"numeric"`` oder ``"text"``.
    """

    name: str
    kind: str
    count: int
    missing: int
    minimum: float | None
    maximum: float | None
    mean: float | None
    unique: int | None


def _is_missing(value: str) -> bool:
    """True für ein leeres oder nur aus Leerzeichen bestehendes Feld."""
    return value.strip() == ""


def _parse_number(value: str) -> float | None:
    """Parst ``value`` als int oder float; ``None``, wenn das nicht gelingt."""
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        return None


def _compute_column(name: str, values: list[str]) -> ColumnStats:
    """Berechnet die Statistik genau einer Spalte."""
    present = [value for value in values if not _is_missing(value)]
    missing = len(values) - len(present)

    numbers: list[float] = []
    numeric = bool(present)
    if numeric:
        for value in present:
            parsed = _parse_number(value)
            if parsed is None:
                numeric = False
                break
            numbers.append(parsed)

    if numeric:
        count = len(numbers)
        mean = round(sum(numbers) / count, 4) if count else None
        return ColumnStats(
            name=name,
            kind="numeric",
            count=count,
            missing=missing,
            minimum=float(min(numbers)) if count else None,
            maximum=float(max(numbers)) if count else None,
            mean=mean,
            unique=None,
        )

    return ColumnStats(
        name=name,
        kind="text",
        count=len(present),
        missing=missing,
        minimum=None,
        maximum=None,
        mean=None,
        unique=len(set(present)),
    )


def compute_stats(table: Table, indices: list[int]) -> list[ColumnStats]:
    """Liefert je Eintrag in ``indices`` eine :class:`ColumnStats` in dieser Reihenfolge.

    Eine Spalte ist genau dann numerisch, wenn sie mindestens einen nicht
    fehlenden Wert enthält und jeder nicht fehlende Wert als int oder float
    parsebar ist; sonst ist sie Text. Fehlende Werte (leer oder nur Leerzeichen)
    werden in ``missing`` gezählt und nicht in Min, Max, Mittelwert und
    Eindeutigkeit berücksichtigt.
    """
    return [
        _compute_column(table.headers[index], [row[index] for row in table.rows])
        for index in indices
    ]

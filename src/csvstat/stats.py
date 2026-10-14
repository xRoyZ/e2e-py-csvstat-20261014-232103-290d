"""Berechnung von Spaltenstatistiken."""

from dataclasses import dataclass

from csvstat import errors
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


def compute_stats(table: Table, indices: list[int]) -> list[ColumnStats]:
    """Liefert je Eintrag in ``indices`` eine :class:`ColumnStats` in dieser Reihenfolge."""
    raise errors.UnimplementedFeature("compute_stats ist noch nicht implementiert.")

"""Auswahl von Spaltenindizes anhand einer Namensliste."""

from csvstat import errors


def select_columns(headers: list[str], spec: str | None) -> list[int]:
    """Wandelt ``spec`` in Spaltenindizes um; ``None`` bedeutet alle Spalten."""
    raise errors.UnimplementedFeature("select_columns ist noch nicht implementiert.")

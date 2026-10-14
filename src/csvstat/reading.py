"""Lesen einer CSV-Datei in eine :class:`Table`."""

from dataclasses import dataclass

from csvstat import errors


@dataclass
class Table:
    """Kopfzeile und Datenzeilen einer CSV-Datei."""

    headers: list[str]
    rows: list[list[str]]


def read_csv(path: str, delimiter: str) -> Table:
    """Liest die CSV-Datei unter ``path`` mit ``delimiter``."""
    raise errors.UnimplementedFeature("read_csv ist noch nicht implementiert.")

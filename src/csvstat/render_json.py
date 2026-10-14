"""JSON-Ausgabe der Spaltenstatistiken.

Die JSON-Schlüssel sind englisch; die Ausgabe ist genau ein JSON-Objekt.
"""

from csvstat import errors
from csvstat.sanitize import sanitize
from csvstat.stats import ColumnStats

__all__ = ["render_json", "sanitize"]


def render_json(path: str, stats: list[ColumnStats]) -> str:
    """Rendert ``stats`` als ein JSON-Objekt für die Datei ``path``."""
    raise errors.UnimplementedFeature("render_json ist noch nicht implementiert.")

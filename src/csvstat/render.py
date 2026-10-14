"""Textbericht der Spaltenstatistiken (deutsch).

Der gemeinsame Sanitizer liegt in :mod:`csvstat.sanitize`; er wird hier
importiert und mit dem Textrenderer geteilt.
"""

from csvstat import errors
from csvstat.render_json import render_json
from csvstat.sanitize import sanitize
from csvstat.stats import ColumnStats

__all__ = ["render_json", "render_text", "sanitize"]


def render_text(path: str, stats: list[ColumnStats]) -> str:
    """Rendert ``stats`` als deutschen Textbericht für die Datei ``path``."""
    raise errors.UnimplementedFeature("render_text ist noch nicht implementiert.")

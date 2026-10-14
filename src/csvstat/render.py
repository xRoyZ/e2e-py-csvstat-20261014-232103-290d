"""Textbericht der Spaltenstatistiken (deutsch).

Der gemeinsame Sanitizer liegt in :mod:`csvstat.sanitize`; er wird hier
importiert und mit dem Textrenderer geteilt.
"""

from csvstat.render_json import render_json
from csvstat.sanitize import sanitize
from csvstat.stats import ColumnStats

__all__ = ["render_json", "render_text", "sanitize"]


def _format_number(value: float) -> str:
    """Formatiert eine Zahl deterministisch mit vier Dezimalstellen und Punkt."""
    return sanitize(f"{value:.4f}")


def render_text(path: str, stats: list[ColumnStats]) -> str:
    """Rendert ``stats`` als deutschen Textbericht für die Datei ``path``.

    Die Ausgabe ist deterministisch: Spalten erscheinen in der Reihenfolge von
    ``stats``, Zahlen nutzen den Punkt als Dezimaltrennzeichen und der Mittelwert
    hat vier Dezimalstellen. Spaltennamen und ausgegebene Werte durchlaufen
    :func:`csvstat.sanitize.sanitize`.
    """
    lines = [f"Datei: {sanitize(path)}"]

    for column in stats:
        lines.append("")
        lines.append(f"Spalte: {sanitize(column.name)}")
        lines.append(f"  Typ: {sanitize(column.kind)}")
        lines.append(f"  Anzahl: {column.count}")
        lines.append(f"  Fehlend: {column.missing}")

        if column.kind == "numeric":
            if column.minimum is not None:
                lines.append(f"  Minimum: {_format_number(column.minimum)}")
            if column.maximum is not None:
                lines.append(f"  Maximum: {_format_number(column.maximum)}")
            if column.mean is not None:
                lines.append(f"  Mittelwert: {_format_number(column.mean)}")
        elif column.unique is not None:
            lines.append(f"  Eindeutig: {column.unique}")

    return "\n".join(lines)

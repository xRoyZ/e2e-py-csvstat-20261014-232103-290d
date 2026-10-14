"""Vollständige Fehlerhierarchie von csvstat.

Alle von der CLI behandelten Fehler erben von :class:`CsvstatError`. Die CLI
schreibt ``str(exc)`` nach stderr und beendet sich mit Exit-Code 2.
"""


class CsvstatError(Exception):
    """Basisklasse für alle behandelten csvstat-Fehler."""


class InputError(CsvstatError):
    """Fehlende, nicht lesbare oder leere Eingabedatei."""


class ParseError(CsvstatError):
    """Fehlerhafte Datenzeile; ``line`` ist die 1-basierte Zeilennummer."""

    def __init__(self, line: int, message: str | None = None) -> None:
        self.line = line
        if message is None:
            message = f"Ungültige Datenzeile in Zeile {line}."
        super().__init__(message)


class ColumnError(CsvstatError):
    """Unbekannter Spaltenname; ``name`` ist der angeforderte Spaltenname."""

    def __init__(self, name: str, message: str | None = None) -> None:
        self.name = name
        if message is None:
            message = f"Unbekannte Spalte: {name}."
        super().__init__(message)


class UnimplementedFeatureError(CsvstatError):
    """Platzhalter-Fehler für noch nicht implementierte Funktionen."""


# Vertragsname aus der geteilten Schnittstelle (ruff N818-konform als Alias).
UnimplementedFeature = UnimplementedFeatureError

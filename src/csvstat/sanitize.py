"""Gemeinsamer Schutz der Ausgabe vor Steuerzeichen.

Reine Zeichenketten-Transformation ohne CSV- oder Statistikwissen; beide
Renderer (Text und JSON) verwenden denselben Helfer.
"""

_CONTROL_CODES = frozenset(range(0x00, 0x20)) | frozenset(range(0x7F, 0xA0))


def sanitize(text: str) -> str:
    """Entfernt Steuerzeichen (u. a. ESC 0x1B) aus ``text``.

    Die Eingabe bleibt ansonsten unverändert; Rückgabe ist immer eine
    Zeichenkette.
    """
    if not text:
        return ""
    return "".join(ch for ch in text if ord(ch) not in _CONTROL_CODES)

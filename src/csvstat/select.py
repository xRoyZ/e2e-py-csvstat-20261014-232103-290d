"""Auswahl von Spaltenindizes anhand einer Namensliste."""

from csvstat import errors


def select_columns(headers: list[str], spec: str | None) -> list[int]:
    """Wandelt ``spec`` in Spaltenindizes um; ``None`` bedeutet alle Spalten.

    ``spec`` ist eine kommagetrennte Liste von Spaltennamen. Jeder Name wird
    von umgebendem Leerraum befreit und auf seinen Index in ``headers``
    abgebildet; die Reihenfolge aus ``spec`` bleibt erhalten. Ein Name, der
    nicht in ``headers`` vorkommt, löst :class:`errors.ColumnError` aus.
    """
    if spec is None:
        return list(range(len(headers)))

    indices: list[int] = []
    for raw_name in spec.split(","):
        name = raw_name.strip()
        if name not in headers:
            raise errors.ColumnError(name)
        indices.append(headers.index(name))
    return indices

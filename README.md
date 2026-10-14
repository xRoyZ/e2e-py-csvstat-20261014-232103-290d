# csvstat

`csvstat` ist ein kleines Kommandozeilenwerkzeug, das eine CSV-Datei einliest
und je Spalte Statistiken auf stdout ausgibt. Für numerische Spalten werden
Anzahl, Minimum, Maximum, Mittelwert und die Anzahl fehlender Werte ausgegeben,
für Textspalten die Anzahl eindeutiger Werte. Die Ausgabe erfolgt wahlweise als
deutscher Textbericht oder als JSON-Objekt.

## Tech-Stack

- Python 3.11+
- `argparse` (Standardbibliothek) für die Kommandozeile
- `csv`-Modul der Standardbibliothek (Encoding `utf-8-sig`) zum Einlesen
- `json` (Standardbibliothek) für die JSON-Ausgabe
- `pytest` für Tests, `ruff` für Linting/Formatierung

Es gibt keine externen Laufzeit-Abhängigkeiten.

## Installation

Empfohlen in einer virtuellen Umgebung:

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
python -m pip install -e ".[dev]"
```

Damit wird das Konsolen-Skript `csvstat` installiert und die Entwicklungs-Tools
(`pytest`, `ruff`) stehen zur Verfügung.

Ohne Installation kann die CLI auch direkt aus dem Quellverzeichnis gestartet
werden:

```bash
python -m csvstat --help
```

## Ausführen

Als installiertes Konsolen-Skript:

```bash
csvstat daten.csv
csvstat --delimiter ";" daten.csv
csvstat --columns name,alter daten.csv
csvstat --json daten.csv
csvstat --help
```

Alternativ als Modul:

```bash
python -m csvstat daten.csv
```

## CLI-Optionen

| Option | Bedeutung |
| --- | --- |
| `datei` | Pfad zur einzulesenden CSV-Datei (Positionsargument, erforderlich). |
| `--delimiter ZEICHEN` | Trennzeichen der CSV-Datei. Standard ist `,`. Die Folge `\t` steht für ein Tabulatorzeichen. |
| `--columns A,B` | Gibt nur die genannten Spalten in der angegebenen Reihenfolge aus. Ohne Angabe werden alle Spalten in Dateireihenfolge ausgegeben. |
| `--json` | Gibt das Ergebnis als JSON-Objekt statt als Textbericht aus. Die JSON-Schlüssel sind englisch. |
| `--help` | Zeigt die Hilfe mit allen Optionen an und beendet mit Exit-Code 0. |

## Exit-Codes

| Code | Bedeutung |
| --- | --- |
| `0` | Erfolgreicher Lauf. |
| `2` | Behandelter Fehler (z. B. fehlende, leere oder fehlerhafte Datei, unbekannter Spaltenname). Die Meldung steht auf stderr, stdout bleibt leer. |

## Tests und Linting

```bash
python -m pytest
ruff format .
ruff check .
```

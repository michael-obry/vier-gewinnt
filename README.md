# Vier Gewinnt mit Alpha-Beta-Pruning

## Projektübersicht

Dieses Projekt implementiert das klassische Spiel **"Vier Gewinnt"** mit einem **KI-Gegner**, der den **Alpha-Beta-Pruning-Algorithmus** verwendet, 
um optimale Züge zu berechnen. Der Algorithmus ist eine optimierte Version des Minimax-Algorithmus und wird verwendet, um die Entscheidungsfindung 
der KI zu verbessern, indem nicht notwendige Knoten im Spielbaum abgeschnitten werden.

Dieses Projekt wurde entwickelt, um meine Fähigkeiten in den Bereichen **künstliche Intelligenz (KI)**, **algorithmische Optimierung** und **Python-Programmierung** 
zu demonstrieren.

## Funktionsweise

Der **Alpha-Beta-Pruning-Algorithmus** durchsucht den Spielbaum, der alle möglichen Züge und deren Auswirkungen darstellt. Durch das Pruning werden Zweige, 
die für die Entscheidungsfindung irrelevant sind, abgeschnitten, was die Effizienz des Minimax-Algorithmus erheblich steigert. 
Dies ermöglicht der KI, schneller und trotzdem effektiv auf die Spielzüge des menschlichen Gegners zu reagieren.

## Installation

### Voraussetzungen

- **Python 3.x**
- Abhängigkeiten, die mit `pip` installiert werden können (siehe unten)

### Installationsschritte

1. **Repository klonen**:
   ```bash
   git clone https://github.com/michael-obry/vier-gewinnt.git
   ```

2. **Projektverzeichnis wechseln**:
   ```bash
   cd vier-gewinnt
   ```

3. **Abhängigkeiten installieren**:
   Installiere die notwendigen Bibliotheken:
   ```bash
   pip install -r requirements.txt
   ```


## Nutzung

Um das Spiel zu starten, führe das folgende Skript im Terminal aus:
```bash
python __main__.py
```

### Spielmodi:

- **Mensch vs. KI**: Spiele gegen den KI-Gegner, der den Alpha-Beta-Pruning-Algorithmus verwendet.
- **Mensch vs. Mensch**: Zwei Spieler können gegeneinander spielen.

## Beispiel

Nach dem Start des Spiels wird ein Raster angezeigt, in das die Spieler abwechselnd ihre Züge eingeben. Die KI berechnet ihre Züge mit Hilfe des 
Alpha-Beta-Pruning-Algorithmus.

Beispielausgabe:
```
 1 2 3 4 5 6 7 8
 ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓
| | | | | | | | |
| | | | | | | | |
| | | | | | | | |
| | | | | | | | |
| | | | | |O| | |
| | | |O|O|O|O| |
| | | |O|O|O|O|O|
| | |O|O|O|O|O|O|
 1 2 3 4 5 6 7 8
```

Der Spieler wählt eine Spalte (1-8), und der KI-Gegner reagiert entsprechend.

## Technische Details

### Alpha-Beta-Pruning
Der **Alpha-Beta-Pruning-Algorithmus** ist eine Optimierung des **Minimax-Algorithmus**, der in der Spieltheorie verwendet wird. Er reduziert die Anzahl 
der Knoten, die im Spielbaum betrachtet werden müssen, und verbessert so die Effizienz der Entscheidungsfindung.

- **Minimax**: Der Algorithmus bewertet die Züge für den Spieler und die KI, indem er versucht, den besten Zug für sich selbst und den schlechtesten für den Gegner zu finden.
- **Alpha-Beta-Pruning**: Dieser Algorithmus "schneidet" unnötige Teile des Entscheidungsbaums ab, wodurch die Berechnungszeit verkürzt wird, ohne das Endergebnis zu beeinflussen.

### Spiellogik
- Das Spiel wird in einem **8x8-Raster** gespielt. Ziel ist es, vier Spielsteine in einer Reihe (horizontal, vertikal oder diagonal) zu platzieren.
- Die KI verwendet den Alpha-Beta-Pruning-Algorithmus, um ihre Entscheidungen zu treffen, wobei der Spielbaum für alle möglichen zukünftigen Züge durchsucht wird.

## Mitwirkung

Beiträge zu diesem Projekt sind willkommen! Falls du Fehler findest oder Ideen zur Verbesserung hast, erstelle gerne einen Pull Request oder eröffne ein Issue.

### Wie beitragen:
1. **Repository forken**.
2. Änderungen vornehmen und committen.
3. Einen **Pull Request** öffnen.

## Lizenz

Dieses Projekt ist unter der **MIT-Lizenz** lizenziert. Weitere Informationen findest du in der [LICENSE](LICENSE) Datei.

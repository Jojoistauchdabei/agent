# Sprachassistent (Voice Assistant) (sprachssistent.py)

Ein KI-gestützter Sprachassistent, der Spracheingaben verarbeitet, mit einem KI-Modell kommuniziert und Antworten als Sprachausgabe wiedergibt.

## Features

- 🎤 Spracheingabe über Mikrofon
- 🔄 Umwandlung von Sprache in Text (Speech-to-Text)
- 🤖 Verarbeitung durch Mixtral-8x7b KI-Modell
- 🔊 Umwandlung der KI-Antwort in Sprache (Text-to-Speech)
- 🌍 Vollständig auf Deutsch

## Voraussetzungen

- Python 3.9
- Mikrofon
- Lautsprecher
- Internetverbindung
- API-Zugang für das KI-Modell
- mpg321, ffmpeg muss installiert sein

## Verwendung

1. Programm starten:
```bash
python sprachassistent.py
```
2. Warten auf die "Bitte sprechen Sie jetzt..." Aufforderung
3. Frage oder Anweisung sprechen
4. KI-Antwort wird automatisch vorgelesen

## Technische Details

Der Assistent nutzt folgende Technologien:
- Google Speech Recognition für Speech-to-Text
- Mixtral-8x7b als KI-Modell
- gTTS (Google Text-to-Speech) für die Sprachausgabe
- mpg321 für die Audiowiedergabe



# KI-Model funktionen (tools.py)

Funktionen:
- Urzeit
- Bildgenerieren
- tts (hörbücher, etc)
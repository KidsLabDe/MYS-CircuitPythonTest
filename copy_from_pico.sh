#!/bin/bash

# Überprüfen, ob /Volumes/CIRCUITPY vorhanden ist, andernfalls /run/media/KingBBQ/CIRCUITPY verwenden
if [ -d "/Volumes/CIRCUITPY" ]; then
	PICO_PATH="/Volumes/CIRCUITPY"
else
	PICO_PATH="/run/media/KingBBQ/CIRCUITPY"
fi

# Zielverzeichnis (aktuelles Verzeichnis)
TARGET_DIR="."

# Kopieren Sie alle Dateien vom Pico in das aktuelle Verzeichnis
rsync -av --progress --exclude ".*" --exclude '*.mpy' --exclude '*.sh' --exclude '_*'  "$PICO_PATH/" "$TARGET_DIR/"

echo "Alle Dateien wurden erfolgreich vom Pico in das aktuelle Verzeichnis kopiert."


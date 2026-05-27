#!/bin/bash
# Preuzima hrLex 1.3 i OpenSubtitles HR frekvencijsku listu.
# Sprema u data/raw/ (nije u git repozitoriju).

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
DATA_RAW="$REPO_ROOT/data/raw"

mkdir -p "$DATA_RAW"

echo "=== Geslar Tools: Preuzimanje izvora ==="
echo "Odredište: $DATA_RAW"
echo ""

# hrLex 1.3 — CLARIN.si repozitorij
HRLEX_URL="https://www.clarin.si/repository/xmlui/bitstream/handle/11356/1232/hrLex_v1.3.tgz"
HRLEX_ARCHIVE="$DATA_RAW/hrLex.tgz"

if [ -f "$DATA_RAW/hrLex_v1.3.txt" ]; then
    echo "[1/2] hrLex 1.3 već postoji — preskačem."
else
    echo "[1/2] Preuzimam hrLex 1.3 (~180 MB)..."
    curl -L --progress-bar -o "$HRLEX_ARCHIVE" "$HRLEX_URL"

    echo "Raspakiravam hrLex..."
    tar -xzf "$HRLEX_ARCHIVE" -C "$DATA_RAW/"

    # Pronađi raspakiranu txt datoteku
    HRLEX_TXT=$(find "$DATA_RAW" -name "hrLex*.txt" | head -1)
    if [ -z "$HRLEX_TXT" ]; then
        echo "GREŠKA: hrLex .txt datoteka nije pronađena u $DATA_RAW"
        echo "Sadržaj:"
        ls -la "$DATA_RAW/"
        exit 1
    fi

    echo "hrLex raspakiran: $(basename "$HRLEX_TXT")"
    LINES=$(wc -l < "$HRLEX_TXT")
    echo "Broj linija: $LINES"
fi

# OpenSubtitles HR frekvencijska lista — hermitdave/FrequencyWords
OPENSUBS_URL="https://raw.githubusercontent.com/hermitdave/FrequencyWords/master/content/2018/hr/hr_50k.txt"
OPENSUBS_FILE="$DATA_RAW/hr_50k.txt"

if [ -f "$OPENSUBS_FILE" ]; then
    echo "[2/2] OpenSubtitles lista već postoji — preskačem."
else
    echo "[2/2] Preuzimam OpenSubtitles HR frekvencijsku listu..."
    curl -L --progress-bar -o "$OPENSUBS_FILE" "$OPENSUBS_URL"
    LINES=$(wc -l < "$OPENSUBS_FILE")
    echo "OpenSubtitles lista: $LINES linija"
fi

echo ""
echo "=== Gotovo ==="
echo "Datoteke u $DATA_RAW:"
ls -lh "$DATA_RAW/"

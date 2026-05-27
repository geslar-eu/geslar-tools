#!/usr/bin/env python3
"""
Izvoz finalne wordliste u JS format kompatibilan s geslar-web/core.js.

Ulaz:  data/final_wordlist.txt
Izlaz: stdout  (preusmjeri: python 05_izvoz_js.py > output_words.js)

Na stderr: summary (N rijeci, entropija za 3/4/5 rijeci).

Format izlaza:
  const WORDS = [
    "abc", "abd", "abe", "abf", ...  // 12 po redu
  ];
"""

import sys
import math
from datetime import date
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent.parent
INPUT_FILE = REPO_ROOT / "data" / "final_wordlist.txt"

WORDS_PER_LINE = 12


def calc_entropy(pool: int, k: int) -> float:
    bits = 0.0
    for i in range(k):
        n = pool - i
        if n > 0:
            bits += math.log2(n)
    return bits


def main():
    if not INPUT_FILE.exists():
        print(f"GREŠKA: {INPUT_FILE} ne postoji.", file=sys.stderr)
        print("Pokreni 04_provjera_kvalitete.py prvo.", file=sys.stderr)
        sys.exit(1)

    with open(INPUT_FILE, encoding="utf-8") as f:
        words = [line.strip() for line in f if line.strip()]

    words.sort()
    n = len(words)
    today = date.today().isoformat()

    entropy_3 = calc_entropy(n, 3)
    entropy_4 = calc_entropy(n, 4)
    entropy_5 = calc_entropy(n, 5)

    # JS output na stdout
    print(f"// Geslar wordlist — generirano: {today}")
    print(f"// Broj rijeci: {n:,}")
    print(f"// Entropija: 3 rij. = {entropy_3:.1f} bita | 4 rij. = {entropy_4:.1f} bita | 5 rij. = {entropy_5:.1f} bita")
    print(f"// Izvor: hrLex 1.3 (CC BY-SA 4.0, CLARIN.si)")
    print(f"// Frekvencijski filter: OpenSubtitles HR (hermitdave/FrequencyWords, CC BY-SA 4.0)")
    print(f"// Metodologija: geslar-tools/METODOLOGIJA.md")
    print(f"// Licenca wordliste: CC BY-SA 4.0 (nasljeđuje hrLex 1.3)")
    print()
    print("const WORDS = [")

    for i in range(0, n, WORDS_PER_LINE):
        chunk = words[i:i + WORDS_PER_LINE]
        quoted = [f'"{w}"' for w in chunk]
        line = "  " + ", ".join(quoted)
        # Dodajemo zarez samo ako nije zadnji red
        if i + WORDS_PER_LINE < n:
            line += ","
        print(line)

    print("];")

    # Summary na stderr
    print(f"\n=== Summary ===", file=sys.stderr)
    print(f"Rijeci:     {n:,}", file=sys.stderr)
    print(f"Entropija:", file=sys.stderr)
    print(f"  3 rijeci: {entropy_3:.1f} bita {'✓' if entropy_3 >= 38 else '⚠️'}", file=sys.stderr)
    print(f"  4 rijeci: {entropy_4:.1f} bita {'✓' if entropy_4 >= 50 else '⚠️'}", file=sys.stderr)
    print(f"  5 rijeci: {entropy_5:.1f} bita ✓", file=sys.stderr)


if __name__ == "__main__":
    main()

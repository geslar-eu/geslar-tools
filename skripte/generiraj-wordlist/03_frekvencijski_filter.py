#!/usr/bin/env python3
"""
Frekvencijski filter — zadržava samo lemme koje se pojavljuju
u top-N najfrekventnijih hrvatskih riječi (OpenSubtitles corpus).

Ulaz:  data/filtered_lemmas.txt
       data/raw/hr_50k.txt  (format: "word count" po liniji)
Izlaz: data/freq_filtered.txt

Matchanje je case-insensitive, ali se sprema originalni oblik iz hrLex.
"""

import sys
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent.parent
LEMMAS_FILE = REPO_ROOT / "data" / "filtered_lemmas.txt"
FREQ_FILE = REPO_ROOT / "data" / "raw" / "hr_50k.txt"
OUTPUT_FILE = REPO_ROOT / "data" / "freq_filtered.txt"


def load_freq_words(freq_file: Path, top_n: int) -> set[str]:
    """Učitava top-N rijeci iz OpenSubtitles liste."""
    words: set[str] = set()
    count = 0

    with open(freq_file, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # hermitdave format: "word count" (razmak, ne tab)
            # Pokušavamo oba separatora
            parts = line.split("\t") if "\t" in line else line.split(" ")
            if len(parts) < 2:
                continue

            word = parts[0].strip().lower()
            words.add(word)
            count += 1

            if count >= top_n:
                break

    return words


def main():
    parser = argparse.ArgumentParser(
        description="Frekvencijski filter wordliste"
    )
    parser.add_argument(
        "--top-n",
        type=int,
        default=30000,
        help="Koliko najfrekventnijih rijeci zadrzati (default: 30000)",
    )
    args = parser.parse_args()

    if not LEMMAS_FILE.exists():
        print(f"GREŠKA: {LEMMAS_FILE} ne postoji.", file=sys.stderr)
        print("Pokreni 02_filtriraj_leme.py prvo.", file=sys.stderr)
        sys.exit(1)

    if not FREQ_FILE.exists():
        print(f"GREŠKA: {FREQ_FILE} ne postoji.", file=sys.stderr)
        print("Pokreni 01_preuzmi_izvore.sh za preuzimanje.", file=sys.stderr)
        sys.exit(1)

    print(f"Ulaz lemmi: {LEMMAS_FILE}")
    print(f"Frekvencijska lista: {FREQ_FILE}")
    print(f"Top-N: {args.top_n:,}")
    print()

    print(f"Učitavam top-{args.top_n:,} najfrekventnijih riječi...")
    freq_set = load_freq_words(FREQ_FILE, args.top_n)
    print(f"Učitano: {len(freq_set):,} jedinstvenih oblika")

    with open(LEMMAS_FILE, encoding="utf-8") as f:
        lemmas = [line.strip() for line in f if line.strip()]

    print(f"Ulaznih lemmi: {len(lemmas):,}")

    filtered = []
    for lemma in lemmas:
        if lemma.lower() in freq_set:
            filtered.append(lemma)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for lemma in filtered:
            f.write(lemma + "\n")

    pct = len(filtered) / len(lemmas) * 100 if lemmas else 0
    print()
    print("=== Rezultati ===")
    print(f"Ulaz:              {len(lemmas):>8,}")
    print(f"Izlaz (u top-{args.top_n // 1000}k): {len(filtered):>8,}")
    print(f"Zadržano:          {pct:>8.1f}%")
    print()
    print(f"Zapisano u: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()

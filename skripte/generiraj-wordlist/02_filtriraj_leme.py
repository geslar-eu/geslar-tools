#!/usr/bin/env python3
"""
Filtrira hrLex 1.3 morfološki leksikon — izvlači kanonske oblike
zajedničkih imenica i pridjeva u nominativu jednine.

Ulaz:  data/raw/hrLex_v1.3.txt  (tab-separated: wordform\tlemma\tMSD)
Izlaz: data/filtered_lemmas.txt  (jedna lemma po liniji)

MULTEXT-East V6 MSD tagset:
  Nc.sn = zajednička imenica, jednina, nominativ
  Agpmsn = pridjev, pozitiv, muški rod, jednina, nominativ
"""

import sys
import glob
import os
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent.parent
DATA_RAW = REPO_ROOT / "data" / "raw"
OUTPUT_FILE = REPO_ROOT / "data" / "filtered_lemmas.txt"


def find_hrlex_file() -> Path:
    patterns = [
        str(DATA_RAW / "hrLex*.txt"),
        str(DATA_RAW / "hrlex*.txt"),
        str(DATA_RAW / "*.txt"),
    ]
    for pattern in patterns:
        matches = glob.glob(pattern)
        if matches:
            # Preferiramo najveću datoteku (hrLex je ~60+ MB)
            matches.sort(key=os.path.getsize, reverse=True)
            return Path(matches[0])
    return None


def is_noun_nominative_singular(msd: str) -> bool:
    # N = imenica, c = zajednička, [2] = rod (m/f/n), [3] = s (singular), [4] = n (nominativ)
    if len(msd) < 5:
        return False
    return (
        msd[0] == 'N'
        and msd[1] == 'c'
        and msd[3] == 's'
        and msd[4] == 'n'
    )


def is_adj_nominative_singular_masc(msd: str) -> bool:
    # Agpmsn[y/n] = pridjev, pozitiv, muški rod, jd., nominativ, određeni/neodređeni
    return msd.startswith('Agpmsn')


def main():
    hrlex_file = find_hrlex_file()
    if hrlex_file is None:
        print("GREŠKA: hrLex .txt datoteka nije pronađena u data/raw/", file=sys.stderr)
        print("Pokreni 01_preuzmi_izvore.sh za preuzimanje.", file=sys.stderr)
        sys.exit(1)

    print(f"Ulaz: {hrlex_file}")
    print(f"Izlaz: {OUTPUT_FILE}")
    print()

    total_lines = 0
    malformed = 0
    canonical_skip = 0
    nouns_found = 0
    adjs_found = 0
    lemmas: set[str] = set()

    with open(hrlex_file, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue
            total_lines += 1

            parts = line.split("\t")
            if len(parts) < 3:
                malformed += 1
                continue

            wordform, lemma, msd = parts[0], parts[1], parts[2]

            # Zadržavamo samo kanonski oblik (wordform == lemma)
            if wordform != lemma:
                canonical_skip += 1
                continue

            if is_noun_nominative_singular(msd):
                nouns_found += 1
                lemmas.add(lemma)
            elif is_adj_nominative_singular_masc(msd):
                adjs_found += 1
                lemmas.add(lemma)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    sorted_lemmas = sorted(lemmas)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for lemma in sorted_lemmas:
            f.write(lemma + "\n")

    print("=== Statistike ===")
    print(f"Ukupno linija parsiranih:    {total_lines:>10,}")
    print(f"Neispravni format:           {malformed:>10,}")
    print(f"Preskočeni (wordform!=lemma):{canonical_skip:>10,}")
    print(f"Imenice pronađene:           {nouns_found:>10,}")
    print(f"Pridjevi pronađeni:          {adjs_found:>10,}")
    print(f"Ukupno unique lemmi:         {len(lemmas):>10,}")
    print()
    print(f"Zapisano u: {OUTPUT_FILE}")
    print()
    print("Primjeri (prvih 20):")
    for lemma in sorted_lemmas[:20]:
        print(f"  {lemma}")


if __name__ == "__main__":
    main()

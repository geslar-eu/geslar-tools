#!/usr/bin/env python3
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
"""
Provjera kvalitete i finalni filteri wordliste.

Ulaz:  data/freq_filtered.txt
Izlaz: data/final_wordlist.txt

Filteri (redom):
  1. Duljina: MIN_LEN=4, MAX_LEN=10
  2. Samo mala slova + hrvatska dijakritika (bez brojeva, crtice, itd.)
  3. Stop words (data/stopwords_hr.txt ili ugrađeni minimalni set)
  4. Profanity lista (ugrađena)

NAPOMENA: 4-char prefix uniqueness (BIP39 standard) namjerno je IZOSTAVLJEN.
  - BIP39 zahtjev postoji zbog autocompleta na hardware walletima (Ledger, Trezor).
  - Geslar je web-based generator — korisnik vidi cijelu riječ, autocomplete nije relevantan.
  - Za Hrvatski, prefix-4 filter eliminira ~35% valjanih riječi bez ikakve koristi:
    (npr. 'agencija' i 'agent' dijele prefiks 'agen' → samo bi jedno prošlo).
  - Levenshtein ≥ 3 check u buildPassphrase() (geslar-web/core.js) sprječava
    generiranje vizualno sličnih parova unutar iste fraze — to je dovoljna zaštita.
"""

import sys
import re
import math
from pathlib import Path
from collections import defaultdict

SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent.parent
INPUT_FILE = REPO_ROOT / "data" / "freq_filtered.txt"
STOPWORDS_FILE = REPO_ROOT / "data" / "stopwords_hr.txt"
OUTPUT_FILE = REPO_ROOT / "data" / "final_wordlist.txt"

MIN_LEN = 4
MAX_LEN = 10

# Minimalni set stop words — funkcionalne i gramatičke riječi koje ne pomažu
# pamtljivosti passphrase-a
BUILTIN_STOPWORDS = {
    "ja", "ti", "on", "ona", "ono", "mi", "vi", "oni", "one", "ona",
    "moj", "tvoj", "svoj", "ovaj", "onaj", "taj", "koji", "koja", "koje",
    "neki", "svaki", "jedan", "dva", "tri", "sve", "svi", "sam", "sama",
    "biti", "imati", "moći", "htjeti", "znati", "ići", "doći", "vidjeti",
    "reći", "dati", "uzeti", "kroz", "prema", "zbog", "između", "ispred",
    "iza", "pored", "kraj", "oko", "nad", "pod", "pred", "pri", "bez",
    "samo", "još", "već", "jako", "malo", "puno", "više", "manje",
    "dobro", "loše", "novo", "staro", "veliki", "mali", "dugo", "kratko",
}

# Profanity — replicirano iz geslar-web/core.js (sramotne i uvredljive)
PROFANITY = {
    "kurac", "kurva", "pička", "guzica", "jebati", "jebeni", "picka",
    "kurvin", "sperma", "analnih", "analni", "seks", "seksi", "oralni",
    "jebač", "jebača", "šupak", "šupka", "drolja", "kurvin", "usratio",
    "usrana", "usrani", "sranje", "usranka", "govnar", "govnara",
}

VALID_CHARS_RE = re.compile(r'^[a-zšđčćž]+$')


def load_stopwords() -> set[str]:
    if STOPWORDS_FILE.exists():
        with open(STOPWORDS_FILE, encoding="utf-8") as f:
            custom = {line.strip().lower() for line in f if line.strip()}
        return BUILTIN_STOPWORDS | custom
    return BUILTIN_STOPWORDS


def calc_entropy(pool_size: int, word_count: int) -> float:
    if pool_size <= 1:
        return 0.0
    # Sampling bez ponavljanja: log2(n * (n-1) * ... * (n-k+1))
    bits = 0.0
    for i in range(word_count):
        n = pool_size - i
        if n > 0:
            bits += math.log2(n)
    return bits


def print_sample(label: str, words: list[str], n: int = 20):
    sample = words[:n]
    print(f"  Odbačeni ({label}): {', '.join(sample)}" + (" ..." if len(words) > n else ""))


def main():
    if not INPUT_FILE.exists():
        print(f"GREŠKA: {INPUT_FILE} ne postoji.", file=sys.stderr)
        print("Pokreni 03_frekvencijski_filter.py prvo.", file=sys.stderr)
        sys.exit(1)

    with open(INPUT_FILE, encoding="utf-8") as f:
        words = [line.strip().lower() for line in f if line.strip()]

    print(f"Ulaz: {INPUT_FILE}")
    print(f"Učitano: {len(words):,} lemmi")
    print()

    # Filter 1: Duljina
    step1_out = [w for w in words if MIN_LEN <= len(w) <= MAX_LEN]
    step1_removed = [w for w in words if not (MIN_LEN <= len(w) <= MAX_LEN)]
    print(f"[1] Duljina {MIN_LEN}-{MAX_LEN}: {len(words):,} → {len(step1_out):,} (-{len(step1_removed):,})")
    if step1_removed:
        too_short = [w for w in step1_removed if len(w) < MIN_LEN][:10]
        too_long = [w for w in step1_removed if len(w) > MAX_LEN][:10]
        if too_short:
            print(f"  Prekratke: {', '.join(too_short)}")
        if too_long:
            print(f"  Predugačke: {', '.join(too_long)}")

    # Filter 2: Samo slova + dijakritika
    step2_out = [w for w in step1_out if VALID_CHARS_RE.match(w)]
    step2_removed = [w for w in step1_out if not VALID_CHARS_RE.match(w)]
    print(f"[2] Samo slova+diak.: {len(step1_out):,} → {len(step2_out):,} (-{len(step2_removed):,})")
    if step2_removed:
        print_sample("sadrži br./crtica", step2_removed)

    # Filter 3: Stop words
    stopwords = load_stopwords()
    step3_out = [w for w in step2_out if w not in stopwords]
    step3_removed = [w for w in step2_out if w in stopwords]
    sw_source = "data/stopwords_hr.txt + ugrađeni" if STOPWORDS_FILE.exists() else "ugrađeni"
    print(f"[3] Stop words ({sw_source}): {len(step2_out):,} → {len(step3_out):,} (-{len(step3_removed):,})")
    if step3_removed:
        print_sample("stop words", step3_removed)

    # Filter 4: Profanity
    step4_out = [w for w in step3_out if w not in PROFANITY]
    step4_removed = [w for w in step3_out if w in PROFANITY]
    print(f"[4] Profanity: {len(step3_out):,} → {len(step4_out):,} (-{len(step4_removed):,})")

    # [5] 4-char prefix uniqueness — IZOSTAVLJENO (vidi docstring na vrhu)
    # Informativni prikaz prefix kolizija (bez eliminacije)
    step5_out = step4_out  # prolaze sve

    prefix_map: dict[str, list[str]] = defaultdict(list)
    for w in sorted(step5_out):
        prefix_map[w[:4]].append(w)
    collision_groups = {p: g for p, g in prefix_map.items() if len(g) > 1}
    total_collision_words = sum(len(g) for g in collision_groups.values())
    print(f"[5] 4-char prefix (informativno, bez eliminacije):")
    print(f"    Prefiksa s kolizijama: {len(collision_groups):,} "
          f"(zahvaća {total_collision_words:,} od {len(step5_out):,} rij.)")
    print(f"    Levenshtein ≥ 3 check u generatoru sprječava slične parove u frazi.")
    if collision_groups:
        print(f"    Primjeri: ", end="")
        examples = list(collision_groups.items())[:3]
        print(", ".join(f"'{p}': {'+'.join(g[:3])}" for p, g in examples))

    # Distribucija duljina
    print()
    print("=== Distribucija duljina finalnog skupa ===")
    len_dist: dict[int, int] = defaultdict(int)
    for w in step5_out:
        len_dist[len(w)] += 1
    total = len(step5_out)
    print(f"{'Duljina':>8} | {'Broj':>6} | {'Udio':>6}")
    print("-" * 28)
    for length in sorted(len_dist):
        count = len_dist[length]
        pct = count / total * 100
        print(f"{length:>8} | {count:>6,} | {pct:>5.1f}%")

    # Entropija
    print()
    print("=== Entropija ===")
    pool = len(step5_out)
    print(f"Pool: {pool:,} riječi")
    print(f"{'Br. rij.':>8} | {'Entropija':>10}")
    print("-" * 22)
    for k in range(2, 7):
        h = calc_entropy(pool, k)
        mark = " ✓" if h >= 40 else " ⚠️"
        print(f"{k:>8} | {h:>9.1f} bita{mark}")

    # Spremi
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for w in sorted(step5_out):
            f.write(w + "\n")

    print()
    print(f"Zapisano {len(step5_out):,} riječi u: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Provjera kvalitete i finalni filteri wordliste.

Ulaz:  data/freq_filtered.txt
Izlaz: data/final_wordlist.txt

Filteri (redom):
  1. Duljina: MIN_LEN=4, MAX_LEN=9
  2. Samo mala slova + hrvatska dijakritika (bez brojeva, crtice, itd.)
  3. Stop words (data/stopwords_hr.txt ili ugrađeni minimalni set)
  4. Profanity lista (ugrađena)
  5. 4-char prefix uniqueness (BIP39 princip)
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
MAX_LEN = 9

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

    # Filter 5: 4-char prefix uniqueness
    prefix_map: dict[str, list[str]] = defaultdict(list)
    for w in sorted(step4_out):
        prefix = w[:4]
        prefix_map[prefix].append(w)

    step5_out = []
    collisions: list[tuple[str, list[str]]] = []
    for prefix, group in sorted(prefix_map.items()):
        step5_out.append(group[0])  # Zadržavamo prvu abecednu
        if len(group) > 1:
            collisions.append((prefix, group))

    total_collisions = sum(len(g) - 1 for _, g in collisions)
    print(f"[5] 4-char prefix unique: {len(step4_out):,} → {len(step5_out):,} (-{total_collisions:,})")

    if collisions:
        print(f"  Kolizija prefiksa: {len(collisions):,} (prvih 5):")
        for prefix, group in collisions[:5]:
            kept = group[0]
            dropped = group[1:]
            print(f"    '{prefix}': zadržano '{kept}', odbačeno: {', '.join(dropped)}")

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

    # Provjera kolizija — mora biti 0
    final_prefixes = [w[:4] for w in step5_out]
    assert len(final_prefixes) == len(set(final_prefixes)), "BUG: ostale prefix kolizije!"
    print()
    print(f"4-char prefix kolizija u finalnoj listi: 0 ✓")

    # Spremi
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for w in step5_out:
            f.write(w + "\n")

    print()
    print(f"Zapisano {len(step5_out):,} riječi u: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()

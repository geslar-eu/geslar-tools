#!/usr/bin/env python3
"""
Analiza wordliste — statistike za audit i usporedbu.

Podrzava:
  - JS datoteke s WORDS array (format core.js)
  - Plain TXT datoteke (jedna rijec po liniji)

Upotreba:
  python analiziraj.py <putanja-do-datoteke>
"""

import sys
import re
import math
from pathlib import Path
from collections import Counter, defaultdict

DIACRITICS = set("šđčćž")
HR_DIACRITIC_RE = re.compile(r'[šđčćž]')
IRATI_RE = re.compile(r'irati$')


def calc_entropy(pool: int, k: int) -> float:
    bits = 0.0
    for i in range(k):
        n = pool - i
        if n > 0:
            bits += math.log2(n)
    return bits


def parse_js_words(content: str) -> list[str]:
    """Izvlači WORDS array iz core.js formata."""
    match = re.search(r'const\s+WORDS\s*=\s*\[(.*?)\]', content, re.DOTALL)
    if not match:
        # Pokušaj s varijantama (var, let, WORDS_POOL itd.)
        match = re.search(r'(?:const|let|var)\s+\w*WORDS?\w*\s*=\s*\[(.*?)\]', content, re.DOTALL)
    if not match:
        return []

    array_content = match.group(1)
    words = re.findall(r'"([^"]+)"', array_content)
    return words


def parse_txt_words(content: str) -> list[str]:
    """Parsira plain TXT — jedna rijec po liniji."""
    return [line.strip().lower() for line in content.splitlines() if line.strip()]


def load_words(filepath: Path) -> list[str]:
    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    if filepath.suffix.lower() == ".js":
        words = parse_js_words(content)
        if not words:
            print("UPOZORENJE: Nije pronađen WORDS array u JS datoteci.", file=sys.stderr)
            print("Pokušavam parsirati kao TXT...", file=sys.stderr)
            words = parse_txt_words(content)
    else:
        words = parse_txt_words(content)

    return words


def bar(value: float, max_value: float, width: int = 20) -> str:
    filled = int(value / max_value * width) if max_value > 0 else 0
    return "█" * filled + "░" * (width - filled)


def main():
    if len(sys.argv) < 2:
        print(f"Upotreba: python {Path(__file__).name} <putanja>")
        print("  Primjer: python analiziraj.py ../../geslar-web/core.js")
        sys.exit(1)

    filepath = Path(sys.argv[1])
    if not filepath.exists():
        print(f"GREŠKA: Datoteka ne postoji: {filepath}", file=sys.stderr)
        sys.exit(1)

    words = load_words(filepath)
    if not words:
        print("GREŠKA: Nije pronađena niti jedna riječ.", file=sys.stderr)
        sys.exit(1)

    n = len(words)
    words_lower = [w.lower() for w in words]

    print(f"=== Analiza wordliste: {filepath.name} ===")
    print(f"Ukupno rijeci: {n:,}")
    print()

    # Distribucija duljina
    print("--- Distribucija duljina ---")
    len_counter = Counter(len(w) for w in words_lower)
    max_count = max(len_counter.values())
    avg_len = sum(len(w) for w in words_lower) / n
    print(f"{'Dulj.':>6} | {'Broj':>6} | {'Udio':>6} | Graf")
    print("-" * 50)
    for length in sorted(len_counter):
        count = len_counter[length]
        pct = count / n * 100
        b = bar(count, max_count)
        print(f"{length:>6} | {count:>6,} | {pct:>5.1f}% | {b}")
    print(f"\nProsječna duljina: {avg_len:.1f} znakova")
    print()

    # Entropija
    print("--- Entropija ---")
    print(f"Pool: {n:,} rijeci")
    print(f"{'Br. rij.':>8} | {'Entropija':>12} | Ocjena")
    print("-" * 40)
    for k in range(2, 7):
        h = calc_entropy(n, k)
        if h >= 50:
            grade = "★★★ Odlično"
        elif h >= 40:
            grade = "★★  Dobro"
        elif h >= 30:
            grade = "★   Granično"
        else:
            grade = "    Nedovoljno ⚠️"
        print(f"{k:>8} | {h:>11.1f}b | {grade}")
    print()

    # Dijakritike
    with_diac = [w for w in words_lower if HR_DIACRITIC_RE.search(w)]
    pct_diac = len(with_diac) / n * 100
    print(f"--- Dijakritike ---")
    print(f"S dijakritikama: {len(with_diac):,} ({pct_diac:.1f}%)")
    print(f"Bez dijakritika: {n - len(with_diac):,} ({100 - pct_diac:.1f}%)")
    print()

    # 4-char prefix
    print("--- 4-char prefix analiza ---")
    prefix_counter: dict[str, list[str]] = defaultdict(list)
    for w in sorted(words_lower):
        prefix_counter[w[:4]].append(w)

    collisions = {p: ws for p, ws in prefix_counter.items() if len(ws) > 1}
    total_collision_words = sum(len(ws) - 1 for ws in collisions.values())

    print(f"Ukupno prefiksa: {len(prefix_counter):,}")
    print(f"Kolizija prefiksa: {len(collisions):,} (zahvaća {total_collision_words:,} rijeci)")

    if collisions:
        top_collisions = sorted(collisions.items(), key=lambda x: len(x[1]), reverse=True)[:10]
        print(f"Top 10 prefiksa s kolizijama:")
        for prefix, group in top_collisions:
            print(f"  '{prefix}': {', '.join(group)}")
    else:
        print("  Nema kolizija ✓")
    print()

    # Top 10 najčešćih 4-char prefiksa (po abeceди, ne kolizijama)
    print("--- Top 10 najčešćih 4-char prefiksa ---")
    top_prefixes = Counter(w[:4] for w in words_lower).most_common(10)
    for prefix, count in top_prefixes:
        print(f"  '{prefix}': {count}x")
    print()

    # Glagoli na -irati
    irati_words = [w for w in words_lower if IRATI_RE.search(w)]
    pct_irati = len(irati_words) / n * 100
    print(f"--- Glagoli na -irati ---")
    print(f"Ukupno: {len(irati_words):,} ({pct_irati:.1f}%)")
    if irati_words:
        print(f"Primjeri: {', '.join(irati_words[:10])}" + (" ..." if len(irati_words) > 10 else ""))
    print()

    # Distribucija početnih slova
    print("--- Distribucija početnih slova ---")
    initial_counter = Counter(w[0] for w in words_lower)
    expected_uniform = n / len(initial_counter)
    chi_components = []
    for letter in sorted(initial_counter):
        count = initial_counter[letter]
        pct = count / n * 100
        b = bar(count, max(initial_counter.values()), 15)
        chi_components.append((count - expected_uniform) ** 2 / expected_uniform)
        print(f"  {letter}: {count:>5,} ({pct:>4.1f}%) {b}")

    # Rough ravnomjernost
    chi_sq = sum(chi_components)
    print(f"\nChi-kvadrat (ravnomjernost): {chi_sq:.0f}")
    print(f"(Manji = ravnomjerniji. Savršena uniformnost = 0)")
    print()

    # Sažetak
    print("=== Sažetak ===")
    h3 = calc_entropy(n, 3)
    h4 = calc_entropy(n, 4)
    print(f"Rijeci:          {n:,}")
    print(f"Prosj. duljina:  {avg_len:.1f} znakova")
    print(f"S dijakritikama: {pct_diac:.1f}%")
    print(f"Glagoli -irati:  {pct_irati:.1f}%")
    print(f"Prefix kolizija: {len(collisions):,}")
    print(f"Entropija 3 rij: {h3:.1f} bita {'✓' if h3 >= 38 else '⚠️'}")
    print(f"Entropija 4 rij: {h4:.1f} bita {'✓' if h4 >= 50 else '⚠️'}")


if __name__ == "__main__":
    main()

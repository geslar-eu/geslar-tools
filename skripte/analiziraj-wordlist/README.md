# Skripta: analiziraj.py

Analizira wordlistu iz JS ili TXT formata i ispisuje detaljne statistike.

## Upotreba

```bash
# Analiza postojećeg core.js
python analiziraj.py ../../geslar-web/core.js

# Analiza TXT datoteke (jedna rijec po liniji)
python analiziraj.py data/final_wordlist.txt

# Analiza s prilagođenim poolom
python analiziraj.py output_words.js
```

## Izlaz

- Ukupan broj riječi
- Distribucija duljina
- Entropija za 2-6 riječi
- Postotak s dijakritikama
- Top 10 najčešćih 4-char prefiksa
- Broj kolizija 4-char prefiksa
- Postotak glagola na -irati
- Prosječna duljina
- Distribucija početnih slova

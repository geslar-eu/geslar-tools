# Pipeline: Generiranje Wordliste

Ovaj pipeline transformira hrLex 1.3 morfološki leksikon u wordlistu
kompatibilnu s `geslar-web/core.js` WORDS arrayem.

## Preduvjeti

```bash
python3 --version  # Python 3.8+
curl --version
```

Nema vanjskih Python paketa — koriste se samo standardne biblioteke.

## Trajanje

Ukupno ~5-10 minuta (dominira preuzimanje ~200 MB).

## Koraci

### Korak 1: `01_preuzmi_izvore.sh`

Preuzima:
- **hrLex 1.3** s CLARIN.si repozitorija (~180 MB gzip)
- **OpenSubtitles HR frekvencijska lista** s hermitdave GitHub-a (~3 MB)

Sprema u `data/raw/` (nije u git repozitoriju — vidi `.gitignore`).

```bash
bash 01_preuzmi_izvore.sh
```

### Korak 2: `02_filtriraj_leme.py`

Ulaz: `data/raw/hrLex_v1.3.txt` (ili ekvivalentno ime)  
Izlaz: `data/filtered_lemmas.txt`

**hrLex 1.3 format:**
```
wordform\tlemma\tMSD
```
Primjer:
```
kuca	kuca	Ncfsn
kući	kuća	Ncfsd
kuće	kuća	Ncfsg
```

**MULTEXT-East V6 MSD tagset (relevantni tagovi):**

| Pozicija | Opis | Vrijednost |
|---|---|---|
| 0 | Kategorija | N = imenica, A = pridjev |
| 1 | Vrsta | c = zajednička (noun common) |
| 2 | Rod | m/f/n |
| 3 | Broj | s = jednina, p = množina |
| 4 | Padež | n = nominativ, g = genitiv... |

Filtrirani tagovi:
- **Zajedničke imenice, nominativ, jednina:** `MSD[0]=='N' and MSD[1]=='c' and MSD[3]=='s' and MSD[4]=='n'`
  - Primjer MSD: `Ncmsn` (muška jd. nom.), `Ncfsn` (ženska jd. nom.), `Ncnsn` (srednja jd. nom.)
- **Pridjevi, pozitiv, muški rod, jd., nominativ:** `MSD.startswith('Agpmsn')`

Uvjet: `wordform == lemma` (zadržavamo samo kanonski oblik)

### Korak 3: `03_frekvencijski_filter.py`

Ulaz: `data/filtered_lemmas.txt`, `data/raw/hr_50k.txt`  
Izlaz: `data/freq_filtered.txt`

**OpenSubtitles format** (hermitdave/FrequencyWords):
```
word count
```
(razmak kao separator, ne tab)

Default: top-30.000 najfrekventnijih. Override: `--top-n 20000`

### Korak 4: `04_provjera_kvalitete.py`

Ulaz: `data/freq_filtered.txt`  
Izlaz: `data/final_wordlist.txt`

Sekvencijalni filteri:
1. Duljina 4-9 znakova
2. Samo slova + hrvatska dijakritika (`[a-zšđčćž]+`)
3. Stop words
4. Profanity lista
5. 4-char prefix uniqueness

Detaljni izvještaj nakon svakog filtera.

### Korak 5: `05_izvoz_js.py`

Ulaz: `data/final_wordlist.txt`  
Izlaz: stdout (preusmjeri u datoteku)

```bash
python 05_izvoz_js.py > output_words.js
```

Formatira JS const array identičan postojećem WORDS arrayu u `core.js`.
Summary (broj riječi, entropija) ide na stderr.

## Cijeli pipeline jednom naredbom

```bash
bash 01_preuzmi_izvore.sh && \
python 02_filtriraj_leme.py && \
python 03_frekvencijski_filter.py && \
python 04_provjera_kvalitete.py && \
python 05_izvoz_js.py > output_words.js
```

## Reprodukcija

Za identične rezultate kod ponovnog pokretanja:
- hrLex 1.3 je verzioniran resurs — uvijek isti output
- OpenSubtitles lista je statična (hermitdave 2018 release)
- Pipeline je determinističan (nema random-a, sortirano abecedno)

Vidi [`docs/wordlist/REPRODUKCIJA.md`](../../docs/wordlist/REPRODUKCIJA.md) za detalje.

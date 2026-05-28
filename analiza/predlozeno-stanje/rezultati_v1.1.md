# Analiza predloženog stanja — hrLex pipeline v1.1

Datum: 28.05.2026.  
Status: **Završeno — izmjereni rezultati**

---

## Sažetak

Pipeline v1.1 (top-50k, max10, bez prefix filtera) producirao je **6.583 lema** —
praktički identično projekciji (~6.600). Entropija je u razini EFF Diceware standarda.

| Metrika | Vrijednost |
|---------|-----------|
| Finalni pool | **6.583 lema** |
| Entropija (3 rij.) | **38,1 bita** ✓ |
| Entropija (4 rij.) | **50,7 bita** ✓ |
| Entropija (5 rij.) | **63,4 bita** ✓ |
| Output datoteka | `output_words.js` (549 redaka) |
| Dijakritika | Ispravna (`životinja`, `žvakanje`...) |

---

## Tok podataka (izmjereno)

```
hrLex 1.3 (6,4 M linija)
  → 02_filtriraj_leme.py (MSD filter: Nc + Ag, nominativ jd.)
  → 53.493 lema

  → 03_frekvencijski_filter.py (top-50k)
  → 7.564 lema  (-85,9%)

  → 04_provjera_kvalitete.py
      [1] Duljina 4-10:    filtriranje kratkih/dugih
      [2] Samo slova+diak: filtriranje br./crtica
      [3] Stop words:      filtriranje funk. riječi
      [4] Profanity:       zanemarivo
      [5] 4-char prefix:   informativno (bez eliminacije)
  → 6.583 lema  (-12,9% od koraka 3)

  → 05_izvoz_js.py
  → output_words.js  (549 redaka JS)
```

---

## Usporedba v1.0 vs. v1.1

| Parametar | v1.0 (testirano) | v1.1 (izmjereno) | Razlog promjene |
|-----------|-----------------|-----------------|-----------------|
| Frekvencijski filter | top-30k | top-50k | HR infleksija — nominativ jd. rasprostire se kroz 14 oblika |
| Maksimalna duljina | 9 znakova | 10 znakova | 556 korisnih lema odbačeno bez razloga |
| 4-char prefix uniqueness | DA (eliminacija) | NE (samo info) | Pogrešan kontekst (BIP39 = hardware wallet, ne web) |
| Finalni pool | **2.660 lema** | **6.583 lema** | +147% poboljšanje |
| Entropija (3 rij.) | 34,1 bita | **38,1 bita** | +4,0 bita |
| Entropija (4 rij.) | 45,5 bita | **50,7 bita** | +5,2 bita |

---

## Zašto je v1.0 producirao samo 2.660 lema

### Uzrok 1: Frekvencijski filter (top-30k → top-50k)

HR nominativ jednine ima nižu individualnu frekvenciju od engleskog ekvivalenta
jer se svaki leksem rasprostire kroz **14 flektivnih oblika** (7 padeža × 2 broja).
Leksemi koji bi bili u engleskom top-30k pojavljuju se u HR listi tek na 30k–50k.

```
top-30k: 5.001 prošlo od 53.493  (9,3%)
top-50k: 7.564 prošlo od 53.493  (14,1%)  ← +51% više lema
```

### Uzrok 2: 4-char prefix uniqueness (uklonjeno)

HR je prefiksalno produktivan jezik — prefiksi `pre-`, `pro-`, `pri-`, `ras-`,
`pod-`, `nad-` su morfološki iznimno produktivni. Primjeri kolizija:

- Prefiks `rasp-`: 50 lema → filter zadržava samo 1
- `agencija` + `agent` → oba imaju `agen`
- `aktivan` + `aktivnost` → oba imaju `akti`
- `alergija` + `alergičan` → oba imaju `aler`
- `arhitekt` + `arhiv` → oba imaju `arhi`

Ukupni utjecaj (v1.0): 5.001 → 2.660 (eliminiralo **46,8%** preostalog skupa).

BIP39 prefix zahtjev postoji isključivo zbog hardware walletova — Geslar je web app.
Zamijenjeno Levenshtein ≥ 3 provjerom u `buildPassphrase()`.

### Uzrok 3: Maksimalna duljina (max9 → max10)

Limit od 9 znakova eliminirao je 556 korisnih pridjeva: `planinski`, `plavičasti`,
`kameni`, `brdoviti`, `sunčani`, `jutarnji`, `morski`...

---

## Usporedba s referencama

| Generator | Pool | 3 rij. | 4 rij. | 5 rij. |
|-----------|------|--------|--------|--------|
| EFF Diceware | 7.776 | 38,8b | 51,7b | 64,6b |
| Geslar WORD_POOL (sadašnji) | 6.692 | 38,1b | 50,8b | 63,5b |
| **Geslar hrLex v1.1** | **6.583** | **38,1b** | **50,7b** | **63,4b** |
| Geslar hrLex v1.0 | 2.660 | 34,1b | 45,5b | 56,9b |
| BIP39 | 2.048 | 33,0b | 44,0b | 55,0b |

**Zaključak:** hrLex v1.1 je u razini EFF Diceware standarda uz lingvistički
verificirani leksik (hrLex + OpenSubtitles frekvencije).

---

## Status pipeline skripti

| Skripta | Status | Ključna promjena |
|---------|--------|-----------------|
| `01_preuzmi_izvore.sh` | ✓ bez izmjena | — |
| `02_filtriraj_leme.py` | ✓ bez izmjena | MSD filter ispravan |
| `03_frekvencijski_filter.py` | ✓ ažurirano | default: 30k → **50k** |
| `04_provjera_kvalitete.py` | ✓ ažurirano | MAX_LEN: 9 → **10**; prefix filter: **uklonjen** |
| `05_izvoz_js.py` | ✓ bez izmjena | — |

---

## Sljedeći korak

Pregledati uzorak iz `output_words.js` prije integracije u `geslar-web/core.js`:

1. Nasumični pregled 50–100 lema — nema arhaizama, tehnicizama, previše apstraktnih pojmova
2. Provjera dijakritika u JS datoteci ✓ (već potvrđeno)
3. Nakon odobravanja: zamijeniti `WORDS` array u `geslar-web/core.js`

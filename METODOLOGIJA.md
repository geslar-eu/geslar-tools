# Metodologija — Geslar Wordlist

Verzija: 1.0  
Datum: 27.05.2026.  
Autori: Geslar tim

## 1. Pregled

Geslar wordlist izgrađen je po uzoru na EFF Diceware metodologiju, prilagođenoj
hrvatskom jeziku. Cilj je wordlista koja:

- Daje ≥38 bita entropije za 3 riječi (EFF standard)
- Sadrži poznate, konkretne, lako pamtljive hrvatske riječi
- Podržava unos na mobilnim uređajima (kratke riječi, bez konfuznih parova)
- Poklapa se s lingvistički verificiranim oblicima (hrLex 1.3 kao normativni izvor)

## 2. Princip minimalne kompleksnosti

**Odabrana paradigmatska forma:** nominativ jednine imenica i pridjeva.

Razlog: sigurnost passphrase-a dolazi iz broja mogućih kombinacija (entropija),
ne iz gramatičke složenosti. Korisnik ne treba znati koji padež je "ispravan" —
svaka slučajno odabrana sekvenca jednako je sigurna.

Usporedba:
- EFF Diceware (engleski): neflektirani infinitivi i nominativi, 7.776 riječi
- BIP39 (engleski): 2.048 pažljivo odabranih engleskih riječi
- Geslar (hrvatski): nominativ jd., imenice + pridjevi, ciljni pool ~7.776

## 3. Pipeline u 5 koraka

```
hrLex 1.3 (860k oblika)
    │
    ▼ 02_filtriraj_leme.py
Kanonski oblici + MSD filter
(imenice Nc.sn + pridjevi Agpmsn)
    │
    ▼ 03_frekvencijski_filter.py
Intersect s OpenSubtitles top-30k
(familijarnost korisnicima)
    │
    ▼ 04_provjera_kvalitete.py
  - Duljina 4-9 znakova
  - Samo slova + dijakritika
  - Stop words out
  - Profanity out
  - 4-char prefix uniqueness
    │
    ▼ 05_izvoz_js.py
JS const array za geslar-web/core.js
```

## 4. Kriteriji kvalitete wordliste

Detalji u [`docs/wordlist/KRITERIJI_ODABIRA.md`](docs/wordlist/KRITERIJI_ODABIRA.md).

Skraćeni pregled:

| Kriterij | Vrijednost | Razlog |
|---|---|---|
| Minimalna duljina | 4 znaka | Izbjegavamo jednoznačne kratice |
| Maksimalna duljina | 9 znakova | Mobilno tipkanje, EFF praksa |
| 4-char prefix unique | Da | BIP39 princip, autocomplete |
| Levenshtein distance | ≥3 pri odabiru | Sprječava konfuzne parove |
| Frekvencijski filter | Top-30k | Familijarnost, memorabilnost |
| MSD tag | Nc.sn + Agpmsn | Normativni kanonski oblik |

## 5. Sigurnosni model

Detalji u [`docs/sigurnost/MODEL_PRIJETNJI.md`](docs/sigurnost/MODEL_PRIJETNJI.md).

Geslar ne traži korisnika da pamti složenu lozinku — traži ga da pamti kratku
priču od 3-5 konkretnih, slučajno odabranih hrvatskih riječi. Entropija dolazi
iz veličine skupa i CSPRNG-a, ne iz složenosti.

## 6. Dijalekti

Dijalektalni poolovi su **dodaci** na main pool, ne zamjene. Korisnik koji
aktivira dalmatinski dijalekt dobiva širu bazu iz koje se biraju riječi, čime
se povećava entropija i kulturna autentičnost.

⚠️ Upozorenje: Dubrovački, Slavonski i Zagorski wordliste imaju <100 filtriranih
riječi (4-8 znakova). Jedino-dijalektalni odabir tih varijanata daje entropiju
ispod 18 bita — implementiran `console.warn` u `getActiveWordPool()`.

## 7. Istraživačke praznine

Vidi [`docs/istrazivanje/ISTRAZIVACKE_PRAZNINE.md`](docs/istrazivanje/ISTRAZIVACKE_PRAZNINE.md)
za popis otvorenih istraživačkih pitanja i potencijalnih doprinosa.

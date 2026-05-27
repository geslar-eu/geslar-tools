# Geslar Tools

Istraživački paket i alati za Geslar passphrase generator.

## Svrha

Dokumentira metodologiju, izvore i principe na kojima se temelji Geslar
wordlist i generacijska logika. Namijenjen za:

- Internu reprodukciju i audit wordlista
- Akademsku suradnju (IHJJ, FF Zagreb NLP grupa)
- Grant prijave (HAMAG-BICRO)
- Eventualni znanstveni rad

## Sadržaj

| Direktorij | Opis |
|---|---|
| `docs/wordlist/` | Metodologija odabira, analiza entropije, dijalekti |
| `docs/sigurnost/` | CSPRNG, model prijetnji, usporedba standarda |
| `docs/istraživanje/` | Pregled literature, inflektirani jezici, istraživačke praznine |
| `skripte/generiraj-wordlist/` | Pipeline: preuzimanje → filtriranje → izvoz u JS |
| `skripte/analiziraj-wordlist/` | Analiza postojeće wordliste |
| `analiza/zateceno-stanje/` | Izmjerene statistike trenutne wordliste |
| `analiza/predlozeno-stanje/` | Rezultati nakon hrLex pipeline-a |
| `reference/` | Bibliografija i BibTeX citati |

## Brzi start

Za generiranje nove wordliste iz hrLex 1.3:

```bash
cd skripte/generiraj-wordlist

# Korak 1: preuzmi izvore (~200 MB, ~2 min)
bash 01_preuzmi_izvore.sh

# Korak 2-4: filtriraj (~2 min)
python 02_filtriraj_leme.py
python 03_frekvencijski_filter.py
python 04_provjera_kvalitete.py

# Korak 5: izvezi u JS format
python 05_izvoz_js.py > output_words.js
```

Vidi [`skripte/generiraj-wordlist/README.md`](skripte/generiraj-wordlist/README.md) za detalje.

Za analizu postojeće wordliste:

```bash
python skripte/analiziraj-wordlist/analiziraj.py ../geslar-web/core.js
```

## Zahtjevi

- Python 3.8+
- bash / git-bash (Windows)
- curl

## Status projekta

| Komponenta | Status |
|---|---|
| Analiza zatečenog stanja | Dovršena (27.05.2026.) |
| hrLex pipeline (skripte) | Implementirano |
| hrLex wordlist (rezultati) | Pending |
| Peer review dokumentacije | Pending |

## Licenca

Skripte: MIT  
Dokumentacija: CC BY-SA 4.0  
Wordlista (output): nasljeđuje licencu hrLex 1.3 (CC BY-SA 4.0)

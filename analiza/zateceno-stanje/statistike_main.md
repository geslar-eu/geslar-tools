# Statistike glavne wordliste — zatečeno stanje

Datum analize: 27.05.2026.  
Izvor: `geslar-web/core.js`, WORDS array  
Alat: `skripte/analiziraj-wordlist/analiziraj.py`

## Pregled

| Metrika | Vrijednost |
|---|---|
| Ukupno riječi (raw WORDS array) | 8.192 |
| WORD_POOL (bez dijakritika, ≥3 znaka) | 6.693 |
| WORD_POOL_ALL (s dijakritikama, ≥3 znaka) | 8.191 |
| Prosječna duljina (WORD_POOL) | 8,4 znaka |
| Medijan duljine | 8 znakova |
| Riječi s dijakritikama | 1.498 (18,3%) |
| Glagoli na -irati | 708 (8,6%) |
| Minimalna duljina | 3 znaka |
| Maksimalna duljina | 25 znakova |

## Distribucija duljina

| Duljina | Broj | Udio |
|---|---|---|
| 3 | 39 | 0,5% |
| 4 | 186 | 2,3% |
| 5 | 344 | 4,2% |
| 6 | 836 | 10,2% |
| 7 | 1.195 | 14,6% |
| 8 | 1.681 | 20,5% |
| 9 | 1.534 | 18,7% |
| 10 | 1.006 | 12,3% |
| 11 | 688 | 8,4% |
| 12 | 350 | 4,3% |
| 13 | 186 | 2,3% |
| 14 | 82 | 1,0% |
| 15 | 39 | 0,5% |
| 16+ | 25 | 0,3% |

**Napomena:** Distribucija je normalna (vrh na 8 znakova), ali rep prema duljim
riječima je problematičan. Riječi >9 znakova čine 29,1% poola.

## Problematične kategorije

| Problem | Broj | Udio |
|---|---|---|
| Riječi dulje od 10 znakova | 1.370 | 16,7% |
| Glagoli na -irati | 708 | 8,6% |
| Glagoli na -irati duži od 10 znakova | 439 | 62,0% od svih -irati |
| Non-unique 4-char prefiksi (kolizije) | 1.432 | 17,5% |
| Riječi kraće od 4 znaka | 39 | 0,5% |

### Primjeri problematičnih riječi

**Preduge (>10 znakova):**
- `programirati` (12), `organizirati` (12), `funkcionirati` (13)
- `internacionalizirati` (19), `desinstallirati` (15)

**4-char prefix kolizije (primjer):**
- `prav`: pravnik, pravda, pravilo, pravopis
- `znan`: znanje, znan, znaost (stara forma)

## Entropija

Formula: H = Σ log₂(n-i) za i=0..k-1 (sampling bez ponavljanja)

| Br. riječi | Pool bez diak. | Pool s diak. | Ocjena |
|---|---|---|---|
| 2 | 25,4 bita | 26,0 bita | Nedovoljno ⚠️ |
| 3 | 38,1 bita | 39,0 bita | Granično |
| 4 | 50,8 bita | 52,0 bita | Dobro ✓ |
| 5 | 63,5 bita | 65,0 bita | Odlično ★ |
| 6 | 76,3 bita | 78,0 bita | Odlično ★ |

**NIST preporuka (SP 800-63B):** ≥112 bita za visoku sigurnost,
≥64 bita za srednju. Za online servise s rate-limitingom ≥40 bita je prihvatljivo.

## Zaključci i preporuke

1. **Default 3 riječi daje 38 bita** — granično. Preporuča se povećati default na 4.
2. **1.370 dugi(h) riječi** smanjuje kvalitetu korisničkog iskustva (tipkanje, pamćenje).
3. **708 glagola na -irati** — apstraktne, duže, slabije memorabilnost. Trebaju van.
4. **1.432 prefix kolizija** — korisnici na mobilnom uređaju ne mogu razlikovati
   riječima po prvih 4 tipki. BIP39 standard zahtijeva 0 kolizija.
5. **hrLex pipeline** (vidi `skripte/generiraj-wordlist/`) rješava sve navedene probleme.

Vidi [`analiza/zateceno-stanje/izvjestaj_entropije.md`](izvjestaj_entropije.md)
za detaljnu usporedbu s industrijskim standardima.

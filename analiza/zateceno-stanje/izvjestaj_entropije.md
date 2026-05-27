# Izvještaj entropije — Geslar passphrase generator

Datum: 27.05.2026.  
Verzija: Geslar 1.x (wordlist zatečeno stanje)

## Formula

### Aproksimacija (sampling s ponavljanjem)
```
H_approx = log₂(pool_size) × word_count
```

### Točna formula (Geslar koristi usedWords Set — bez ponavljanja)
```
H_stvarna = log₂(n) + log₂(n-1) + ... + log₂(n-k+1)
           = Σ log₂(n-i)  za i = 0..k-1
```

**Razlika od aproksimacije:** <1 bita za k=3, n=6.693 (zanemariva).

## Geslar entropija — zatečeno stanje

### WORD_POOL (bez dijakritika, 6.693 rij.)

| Br. rij. | H (točna) | H (approx) | Razlika |
|---|---|---|---|
| 2 | 25,4 bita | 25,4 bita | 0,0 |
| 3 | 38,1 bita | 38,1 bita | 0,0 |
| 4 | 50,8 bita | 50,8 bita | 0,0 |
| 5 | 63,5 bita | 63,5 bita | 0,0 |
| 6 | 76,2 bita | 76,2 bita | 0,0 |

### WORD_POOL_ALL (s dijakritikama, 8.191 rij.)

| Br. rij. | H (točna) | H (approx) |
|---|---|---|
| 2 | 26,0 bita | 26,0 bita |
| 3 | 39,0 bita | 39,0 bita |
| 4 | 52,0 bita | 52,0 bita |
| 5 | 65,0 bita | 65,0 bita |
| 6 | 78,0 bita | 78,0 bita |

## Usporedba standarda

| Generator | Jezik | Pool | bit/rij. | 3 rij. | 4 rij. | 5 rij. |
|---|---|---|---|---|---|---|
| EFF Diceware (2016) | Engleski | 7.776 | 12,92 | 38,8 | 51,7 | 64,6 |
| BIP39 (2013) | Engleski | 2.048 | 11,00 | 33,0 | 44,0 | 55,0 |
| niezgadniesz.pl | Poljski | ~5.000 | 12,29 | 36,9 | 49,1 | 61,4 |
| Geslar (bez diak.) | Hrvatski | 6.693 | 12,70 | 38,1 | 50,8 | 63,5 |
| Geslar (s diak.) | Hrvatski | 8.191 | 12,99 | 39,0 | 52,0 | 65,0 |
| **Geslar hrLex*** | **Hrvatski** | **~7.776** | **12,92** | **38,8** | **51,7** | **64,6** |

*Projekcija nakon hrLex pipeline-a (ciljni pool = EFF Diceware ekvivalent)*

## Sigurnosni kontekst

### Online servisi (s rate-limitingom)

Za online servis s rate-limitingom od 10 pokušaja/min:
- Pretraga prostora od 2^38 kombinacija bi trajala **~50.000 godina** brute forceom
- Praktično: zaštićen već s 3 riječima za online scenarij

### Offline napad (password hash)

Pretpostavka: bcrypt napadač može testirati 1.000 hash-eva/sec:

| Pool | 3 rij. | 4 rij. | 5 rij. |
|---|---|---|---|
| 6.693 (bez diak) | 2^38,1 = 341 mlrd. ≈ **4 dana** | 2^50,8 = 1,9×10^15 ≈ **61.000 god.** | Praktično nedosežno |
| 8.191 (s diak.) | 2^39 = 549 mlrd. ≈ **6 dana** | 2^52 = 4,5×10^15 ≈ **143.000 god.** | Nedosežno |

**Zaključak za offline scenarij:** 3 riječi nisu dovoljne za offline zaštitu
passphrase hash-a. 4+ riječi su sigurne čak i uz slabe hash algoritme.

### Password manager master passphrase

Preporuka: 5+ riječi (≥63 bita). Geslar s 5 riječi i pool 8.191 daje 65 bita —
ekvivalentno 20-znaknom random ASCII lozinkom.

## NIST SP 800-63B usklađenost

| Assurance level | Zahtjev | Geslar (4 rij., bez diak) | Zadovoljava? |
|---|---|---|---|
| AAL1 | ≥8 bit | 50,8 bita | ✓ |
| AAL2 | ≥8 bit + MFA | 50,8 bita | ✓ (uz MFA) |
| AAL3 | Hardverski token | N/A | N/A |

## Preporuke

1. **Povećati default s 3 na 4 riječi** — 50 bita je siguran standard za
   sve scenarije bez MFA.
2. **Koristiti WORD_POOL_ALL** (s dijakritikama) ako je UI podešen da ih
   prikazuje — 1,3 bita dodatne entropije besplatno.
3. **hrLex pipeline** ciljano na ~7.776 filtiranih riječi — dostiže EFF Diceware
   razinu uz lingvistički verificirani leksik.

# Analiza entropije — metodologija i izračuni

Verzija: 1.0  
Datum: 27.05.2026.

Vidi i: [`analiza/zateceno-stanje/izvjestaj_entropije.md`](../../analiza/zateceno-stanje/izvjestaj_entropije.md)
za konkretne izmjerene vrijednosti.

## Što je entropija u kontekstu passphrase-a?

Entropija mjeri koliko je kombinacija moguće — tj. koliko je teško pogoditi
passphrase napadom iscrpne pretrage (brute force).

**Formalna definicija za uniform random passphrase:**
```
H = -Σ p(x) × log₂(p(x))
```
Za uniformnu distribuciju (svaka kombinacija jednako vjerojatna):
```
H = log₂(ukupan broj kombinacija)
```

## Geslar model generiranja

Geslar bira `k` riječi iz poola `n` **bez ponavljanja** (koristi `usedWords` Set).
To znači da je svaki potez uvjetovan prethodnim:

```
P(sekvenca od k rijeci) = 1 / (n × (n-1) × ... × (n-k+1))
```

Entropija:
```
H = log₂(n × (n-1) × ... × (n-k+1))
  = Σ log₂(n-i)  za i = 0..k-1
```

**Za k=3, n=6.693:**
```
H = log₂(6693) + log₂(6692) + log₂(6691)
  = 12,705 + 12,704 + 12,703
  = 38,11 bita
```

Razlika od aproksimacije (`H_approx = k × log₂(n) = 38,12`) je < 0,01 bita —
zanemariva.

## Usporedba s alternativnim generatorima

### Slučajni znakovi vs. passphrase

Za usporedbu: nasumična lozinka od 8 lowercase slova (26^8):
```
H = log₂(26^8) = 8 × log₂(26) = 37,6 bita
```
**Geslar 3 rij. ≈ random 8 slova** (36-38 bita). Ali passphrase je mnogo
lakše pamtiti.

### Geslar vs. EFF vs. BIP39

| Generator | Pool | 3 rij. | Tipkanje (3 rij.) | Pamtljivost |
|---|---|---|---|---|
| BIP39 | 2.048 | 33 bita | ~15 zn. | Srednje |
| niezgadniesz.pl | ~5.000 | 36,9 bita | ~18 zn. | Dobro |
| **Geslar** | 6.693 | 38,1 bita | ~25 zn. | Visoko ✓ |
| EFF Diceware | 7.776 | 38,8 bita | ~25 zn. | Visoko ✓ |
| 4 rij. Geslar | 6.693 | 50,8 bita | ~33 zn. | Visoko ✓ |

**Tipkanje:** procjenjeno za prosječnu duljinu 8.4 znakova + razmaci.

## Distribucija poola i entropija

Geslar koristi dvije pool varijante:

### WORD_POOL (bez dijakritika)
Koristimo za: uređaje bez HR tipkovnice, legacy sustave

```
Pool:    6.693 rij.
log₂(n): 12,70 bita/rij.
3 rij.:  38,1 bita
4 rij.:  50,8 bita
```

### WORD_POOL_ALL (s dijakritikama)
Koristimo za: modernne uređaje s HR tipkovnicom

```
Pool:    8.191 rij.
log₂(n): 12,99 bita/rij.
3 rij.:  39,0 bita
4 rij.:  52,0 bita
```

Razlika od 1 bita (6.693 vs. 8.191) dolazi isključivo od 1.498 rij. s
dijakritikama — vrijedi koristiti ako korisnik može upisivati `šđčćž`.

## Entropija i broj pretraga (attack cost)

| Entropija | Kombinacija | bcrypt@1k/s | SHA-256@1B/s |
|---|---|---|---|
| 38 bita | 274 mlrd. | 3 dana | 4,5 min |
| 51 bita | 2,25 × 10^15 | 71.000 god. | 26 dana |
| 64 bita | 1,84 × 10^19 | Nedosežno | 584 god. |

**Zaključak:** Za offline napad s bcryptom, 4 Geslar rijeci (51 bita) je siguran
standard za prekosutrašnji hardware. Za SHA-256 hash napad, 5 rijeci (64 bita)
je preporučeno.

## Predviđanja hrLex pipeline-a

Ciljni pool nakon hrLex pipeline-a: ~7.500-8.000 rij.

```
Pool 7.776 (EFF paritet):
  3 rij.: 38,8 bita  (poboljšanje od 0,7 bita vs. trenutni WORD_POOL)
  4 rij.: 51,7 bita
  5 rij.: 64,6 bita
```

Poboljšanje nije dramatično (+0,7 bita) ali vrijednost hrLex pipeline-a nije
samo u entropiji — nego u lingvističkoj kvaliteti, reproducibilnosti i
dokumentiranoj metodologiji.

# Usporedba passphrase standarda

Verzija: 1.0  
Datum: 27.05.2026.

## Pregled standarda

### EFF Diceware (2016)

**Organizacija:** Electronic Frontier Foundation  
**URL:** https://www.eff.org/deeplinks/2016/07/new-wordlists-random-passphrases

| Parametar | Vrijednost |
|---|---|
| Veličina poola | 7.776 rij. (6^5) |
| bit/rij. | 12,92 |
| Entropija (5 rij.) | 64,6 bita |
| Metoda generiranja | Fizičke kockice (5×d6) ili CSPRNG |
| Jezik | Engleski |
| Kriteriji | Poznate rij., ≤6 zn. preferira, bez uvredljivih |
| Licenca | CC BY 3.0 |

**Prednosti:** Fizičke kockice eliminiraju ovisnost o digitalnom generatoru.
Wordlista je pažljivo ručno kurirana. Zlatni standard za engleski.

**Mane:** Engleske rij. manje memorabilne za ne-engleske govornike. Fizičke
kockice su "friction" — korisnici ih ne koriste.

---

### BIP39 (2013)

**Standard:** Bitcoin Improvement Proposal 39  
**URL:** https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki

| Parametar | Vrijednost |
|---|---|
| Veličina poola | 2.048 rij. (2^11) |
| bit/rij. | 11,00 |
| Entropija (12 rij.) | 132 bita (standard za wallet seed) |
| Metoda generiranja | CSPRNG + checksum |
| Jezik | Engleski (+ 9 prijevoda, nema HR) |
| Kriteriji | ≤8 zn., 4-char prefix unique, Levenshtein ≥3 |
| Licenca | CC0 |

**Prednosti:** Checksum (zadnja rij. je parcijalni hash seedphrase-a) detektira
greške pri unosu. Strogi kriteriji za koristljivost. Podržan hardverski.

**Mane:** 2.048 rij. → samo 11 bita/rij. Za passphrase (ne seed) treba 5+
rij. za adekvatnu sigurnost. Nema HR varijante.

**Geslar razlika:** Geslar ne koristi checksum mehanizam (passphrase nije
seed). Wordlista je ~3× veća od BIP39 — bolja entropija po rij.

---

### NIST SP 800-63B (2017, rev. 2020)

**Organizacija:** National Institute of Standards and Technology  
**URL:** https://pages.nist.gov/800-63-3/sp800-63b.html

Nije wordlista nego **smjernice za autentikaciju**. Relevantne odredbe:

| Parametar | Zahtjev |
|---|---|
| Minimalna duljina lozinke | 8 znakova |
| Preporučena duljina | 64+ znakova |
| Minimum entropije | Nije propisana (odbačena praksa "entropija pravila") |
| Provjera kompromitiranih lozinki | Obavezna |
| Zahtjevi složenosti | Zabranjeni (mješavina vrsta znakova) |

**Geslar usklađenost:**
- ✓ Geslar 4-rij. passphrase ima 33-65 znakova (tipično) → >8 zn.
- ✓ Nema zahtjeva složenosti koji bi zbunjivali korisnike
- ⚠️ Geslar ne provjerava je li passphrase kompromitiran (HaveIBeenPwned)
  — identificirani gap za buduću verziju

---

### niezgadniesz.pl (Polska, ~2020)

**URL:** https://niezgadniesz.pl  
**Jedini dokumentirani analogni slučaj za slavenski jezik**

| Parametar | Vrijednost |
|---|---|
| Jezik | Poljski |
| Pool | ~5.000 rij. |
| bit/rij. | ~12,3 |
| Nominativ jd. | Da |
| MSD filtriranje | Nije dokumentirano |
| Licenca | Nije poznata |

**Relevantnost za Geslar:** Jedini prethodni rad koji rješava isti problem
(inflektirani slavenski jezik + passphrase). Metodologija nije u potpunosti
dokumentirana — Geslar je rigorozniji u opisu pipeline-a.

---

## Matrica usporedbe

| Kriterij | EFF | BIP39 | niezgadniesz | Geslar |
|---|---|---|---|---|
| Pool veličina | 7.776 | 2.048 | ~5.000 | 6.693 |
| bit/rij. | 12,92 | 11,00 | 12,29 | 12,70 |
| Entropija (4 rij.) | 51,7 | 44,0 | 49,1 | 50,8 |
| CSPRNG | Opcionalno | Da | N/P | Da ✓ |
| Prefix unique (4-ch.) | N/P | Da | N/P | Djelomično |
| Levenshtein ≥3 | N/P | Da | N/P | Nije (v1) |
| Morfološki verificirano | Ručno | Ručno | Nepoznato | hrLex 1.3 ✓ |
| Dijalekti | Ne | Ne | Ne | Da ✓ |
| Otvoreni kod | Da | Da | Ne | Da ✓ |
| Dokumentiran pipeline | Djelomično | Da | Ne | Da ✓ |
| EU hositing | N/A | N/A | Da | Da ✓ |

## Pozicioniranje Geslar-a

Geslar je jedina passphrase implementacija koja:

1. Koristi lingvistički verificirani HR leksikon (hrLex 1.3)
2. Podržava dijalektalne varijante kao sigurnosni feature
3. Dokumentira puni reprodukcijski pipeline (open source)
4. Kombinira EFF-razinu entropije s BIP39-razinom tehničkih kriterija
   za slavenski, visoko-fleksijski jezik

**Gap u odnosu na BIP39:** Nedostaje Levenshtein ≥3 filter i checksum.
Identificirani kao ciljevi za v1.1.

# Istraživačke praznine — Geslar i HR passphrase

Verzija: 1.0  
Datum: 27.05.2026.

Ovaj dokument identificira što **ne postoji** u akademskoj literaturi i
javno dostupnim resursima, a što je relevantno za Geslar projekt.
Ovo je **"research novelty" sekcija** za eventualni paper ili grant prijavu.

---

## 1. Nema objavljene metodologije za HR passphrase wordliste

**Status:** Gap — nije pronađen ni jedan peer-reviewed rad ni tehnički
dokument koji opisuje izgradnju wordliste za hrvatski passphrase generator.

**Detalji:** Pretraga ACM Digital Library, IEEE Xplore, arXiv (cs.CR),
CLARIN repozitorij i Google Scholar (2024-2026) nije dala rezultate za
ključne termine:
- "Croatian passphrase"
- "hrvatska lozinka + rječnik"
- "HR wordlist + security"

**Doprinos Geslar-a:** Ovaj repozitorij je (prema dostupnim izvorima)
prva javno dokumentirana metodologija za izgradnju HR passphrase wordliste.
Pipeline je reproducibilan, koristi verificirane javne izvore, i prati
standarde koji su usporedivi s EFF Diceware i BIP39.

---

## 2. Nema strojno-čitljivih dijalektalnih resursa s CC BY-SA licencom

**Status:** Kritični gap za proširenje Geslar dijalektalnih poolova.

**Detalji:**

| Dijalekt | Resursi | Licenca | Strojno čitljivo |
|---|---|---|---|
| Čakavski | Čakavski sabor (fragmenti) | Autorski zaštićeno | Ne |
| Kajkavski | Pergamena (online baza) | Autorski zaštićeno | Ne |
| Istarski | Nema centraliziranog | — | — |
| Međimurski | Nema centraliziranog | — | — |

IHJJ (Institut za hrvatski jezik i jezikoslovlje) ima projekte dijalektalnih
atlasa, ali podaci nisu u CC-kompatibilnim licencama.

**Potencijal za doprinos:** Geslar tim (ili akademski partner) mogao bi
izraditi i publicirati prve strojno-čitljive, CC BY-SA dijalektalne wordliste.
Ovo bi bila znatna donacija za HR NLP zajednicu.

---

## 3. Nema peer-reviewed rada o passphraseima za inflektirane jezike

**Status:** Akademska praznina — jedini analogni slučaj (niezgadniesz.pl za
Poljski) nije peer-reviewed.

**Detalji:** Pretraživanjem literature (ACM, IEEE, USENIX Security,
arXiv cs.CR) nađena su istraživanja za:
- Engleski: EFF Diceware, BIP39, Bonneau et al.
- Kineski: nekoliko radova o karakter-baziranim passphrase
- Arapski: jedan rad (Al-Ameen et al., 2015)
- Slavenski jezici: **nema peer-reviewed radova**

Slavenski jezici (HR, PL, CS, SK, RU, BG) imaju zajedno >300 milijuna
izvornih govornika — i nema akademskog rada o passphrase sigurnosti za ove jezike.

**Research novelty:** Rad koji formalizira "nominativ jednine kao kanonska forma"
za slavenski passphrase, s empirijskim testom retencije, bio bi nov doprinos.

---

## 4. BIP39 za slavenske jezike — nedostaje HR

**Status:** Konkretan gap s jasnim akcijskim potencijalom.

**Detalji:** BIP39 standard (Palatinus & Rusnak, 2013) ima službene prijevode za:
- Engleski, Japanski, Kineski (simpliciran/trad.), Korejski
- Češki (dodan 2021.)
- Slovenački (dodan 2022.)
- Talijanski, Španjolski, Francuski, Portugalski

**Hrvatski nije zastupljen.** Obzirom na Geslar wordlist (hrLex, 4-char
prefix unique, Levenshtein — buduća verzija), postoji tehnička osnova za
BIP39-kompatibilnu HR wordlistu.

**Akcija:** Po završetku Geslar v1.1 (Levenshtein filter + checksum), moguće
je podnijeti BIP pull request s HR wordlistom. To bi bio dokumentiran, javno
vidljiv doprinos blockchain ekosustavu i HR crypto zajednici.

---

## 5. Miješanje dijalekata kao adversarial uncertainty — nema istraživanja

**Status:** Potpuno neistražena oblast.

**Hipoteza (Geslar, 2026.):** Korisnik koji koristi miješani pool (standardni
HR + čakavski + kajkavski) uzrokuje značajno veći trošak za dictionary attack
jer napadač mora pretpostaviti koji dijalekti su aktivni.

**Formalni model (skica):**
```
Napadač koji ne zna aktivne dijalekte mora pretražiti:
  Σ C(8,k) × (kombinacije za k-dijalektni pool)  za k=0..8

= 256 moguće kombinacije dijalekata × prosječna veličina poola
```

**Nema objavljenog modela** za "dijalektalna raznolikost kao security layer".
Jedina referenca: Ur et al. (2023) koja marginalno dotiče temu za arapski,
ali bez formalnog modela.

**Research novelty:** Formalizacija ovog modela (entropija vs. napadačev
knowledge of dialect mix) bio bi novi doprinos u security literaturi.

---

## 6. Nedostatak HR NLP resursa s kriptografskim kriterijima

**Status:** Metodološki gap.

Ni jedan javni HR NLP resurs nije kreiran s kriptografskim kriterijima
na umu:
- hrLex 1.3: morfološki leksikon, bez frekvencijskog ranga
- hrWaC 2.1: web korpus, bez prefix-uniqueness garancija
- CroWN 2.0: WordNet, bez sigurnosnih razmatranja

**Doprinos Geslar-a:** Geslar pipeline je första metodologija koja kombinira
NLP resurse (hrLex, OpenSubtitles) s kriptografskim zahtjevima (entropija,
prefix uniqueness, Levenshtein — buduće).

---

## Sažetak potencijalnih doprinosa

| Gap | Tip doprinosa | Potencijalna mjesta objave |
|---|---|---|
| Metodologija HR wordliste | Tehnički dokument + dataset | CLARIN.si, GitHub |
| Inflektirani jezici + passphrase | Peer-reviewed rad | USENIX Security, CHI |
| BIP39 za HR | BIP pull request | Bitcoin GitHub |
| Dijalekti kao security layer | Kraći rad / workshop | IEEE S&P workshop |
| Strojno-čitljivi HR dijalekti | Dataset + paper | LREC-COLING |

## Kontakti za akademsku suradnju

- **IHJJ** (Institut za HR jezik) — dijalektalni atlasi, normativni leksikoni
- **FF Zagreb, NLP grupa** — hrLex razvoj, CroWN
- **CLARIN.si** — distribucija HR jezičnih resursa
- **HAMAG-BICRO** — grant financiranje za istraživački dio

*Za grant prijavu: Sekcije 1, 3, 4 i 5 su najjači argumenti novelty.*

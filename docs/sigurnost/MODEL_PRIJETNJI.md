# Model prijetnji — Geslar passphrase generator

Verzija: 1.0  
Datum: 27.05.2026.

## Opseg (Scope)

Ovaj model prijetnji pokriva **Geslar passphrase generator** — klijentsku
JavaScript aplikaciju koja generira nasumične passphrase-e od hrvatskih riječi.

**Nije u opsegu:** backend autentikacija servisa koji koristi Geslar passphrase,
pohrana passphrase-a, transport.

## Imovina (Assets)

| Imovina | Klasifikacija | Opis |
|---|---|---|
| Generirani passphrase | Tajno | Primarna zaštićena vrijednost |
| Entropija generiranja | Kritično | Izvor slučajnosti (CSPRNG) |
| Wordlista | Javno | Poznata napadaču (open source) |
| Korisničke postavke | Nisko | Odabir dijalekata, broj rij. |

## Napadači (Threat Actors)

### T1: Napadač koji pogađa passphrase (brute force)

**Pretpostavke napadača:**
- Zna da korisnik koristi Geslar
- Ima pristup Geslar wordlisti (javno dostupna)
- Ne zna koji dijalekti su aktivni
- Ne zna broj odabranih riječi

**Napad:** Iterira sve kombinacije iz poznate wordliste.

**Mitigacija:**
- Entropija ≥38 bita za 3 rij. (dovoljno za online servise s rate-limitingom)
- Entropija ≥50 bita za 4 rij. (dovoljno za offline scenarije s bcryptom)
- Dijalekti povećavaju neizvjesnost za napadača

**Preostali rizik:** Nizak za online servise, srednji za offline s 3 rij.

---

### T2: Napadač koji predviđa output generatora

**Pretpostavke napadača:**
- Ima pristup pregledništu korisnika (XSS, malware)
- Može promatrati neke outpute `Math.random()` i pokušati predvidjeti buduće

**Napad (eliminiran):** `Math.random()` ima predvidljivi state. Napadač koji
promatra seed i neke outpute može rekonstruirati sve buduće slučajne vrijednosti.

**Mitigacija:** Geslar koristi `crypto.getRandomValues()` — OS-razina CSPRNG,
nije predvidljiv ni uz pristup prethodnim outputima.

**Preostali rizik:** Zanemariv. `crypto.getRandomValues()` nema poznatih
kriptografskih ranjivosti.

---

### T3: Napadač koji kompromitira klijentski kod

**Pretpostavke napadača:**
- CDN kompromis (supply chain)
- XSS koji mijenja Geslar JavaScript
- Maliciozni browser extension

**Napad:** Zamjena `cryptoRandIndex()` s predvidljivim generatorom, ili
eksfiltracija generiranog passphrase-a.

**Mitigacija:**
- SRI (Subresource Integrity) za CDN loadanje: `integrity="sha384-..."`
- CSP (Content Security Policy) koji blokira inline skripte
- Geslar je self-hosted — korisnik kontrolira izvođenje koda

**Preostali rizik:** Srednji — zahtijeva infrastrukturni kompromis. Van opsega
generatora, u opsegu hosta.

---

### T4: Napadač koji promatra komunikacijski kanal

**Pretpostavke napadača:**
- MITM napad na HTTP vezu

**Napad:** Presretanje passphrase-a u prijenosu.

**Mitigacija:** Geslar je klijentska aplikacija — passphrase se generira i
**prikazuje lokalno**, bez slanja na server. Nema kommunikacije.

**Preostali rizik:** Zanemariv za generator (nije primjenjivo).

---

### T5: Korisnik koji odabire slab mod

**Prijetnja:** Korisnik aktivira samo mali dijalekt (Dubrovački: ~68 rij.)
i dobiva passphrase s entropijom 18 bita.

**Mitigacija:**
- `console.warn()` za pool < 100 rij. (implementirano 27.05.2026.)
- Planirani UI warn za pool < 500 rij.

**Preostali rizik:** Srednji — korisnik može ignorirati upozorenje. Preporuča
se hard block za izrazito male poolove.

---

## STRIDE analiza

| Prijetnja | Kategorija | Rizik | Mitigirano? |
|---|---|---|---|
| Brute force passphrase-a (3 rij.) | Elevation of Privilege | Srednji | Djelomično |
| Math.random() predict | Elevation of Privilege | Visoki | Da ✓ |
| Supply chain / XSS | Tampering | Visoki | Djelomično |
| Premali pool (korisnik) | Elevation of Privilege | Srednji | Djelomično |
| Passphrase eksfiltracija | Information Disclosure | Visoki | N/A (lokalno) |
| Replay attack | Repudiation | Nizak | N/A |

## Preporuke

1. **Povećati default na 4 rij.** — eliminira "Srednji" brute force rizik.
2. **Implementirati SRI** za sve eksterno učitavane resurse.
3. **Hard block za pool < 100 rij.** — trenutni `console.warn` nije dovoljan.
4. **Security audit wordliste** — provjera da nema rij. koje su trivijalni
   dio standardnih napadačkih rječnika (hr_weak_passwords.txt ekvivalent).

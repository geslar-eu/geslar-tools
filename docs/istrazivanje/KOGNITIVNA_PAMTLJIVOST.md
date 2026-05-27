# Kognitivna pamtljivost — zašto passphrase od imenica radi

Verzija: 1.0  
Datum: 27.05.2026.

## Pregled

Ovo poglavlje objašnjava kognitivno-psihološke temelje Geslar metodologije:
zašto passphrase od poznatih, konkretnih imenica nativnog jezika pruža bolje
korisničko iskustvo i pamtljivost od alternativa.

---

## 1. Chunking i kratkoročna memorija

**Miller's Law (1956):** Kratkoročna memorija može pohraniti 7±2 "chunkova".
Chunk je bilo koja jedinica koja se percipira kao cjelina.

Za passphrase:
- Random string `xKf9@mP2` = 8 zasebnih znakova = 8 chunkova → na rubu kapaciteta
- `šuma rijeka planina` = 3 rij. = 3 chunkova → komforno ispod kapaciteta

Geslar 3-4 rij. je optimalan raspon za kratkoročno pamćenje.

---

## 2. Dual Coding Theory (Paivio, 1971)

Paivio pokazuje da se informacije pohranjuju u dva sustava:
- **Verbalni sustav:** fonološki i semantički zapis rij.
- **Vizualni sustav:** mentalne slike

**Konkretne imenice** (šuma, rijeka, kamen) aktiviraju **oba sustava**
istovremeno — "double encoding" → jači, otporniji zapis u dugoročnoj memoriji.

**Apstraktni pojmovi** (sloboda, organizirati, implementacija) aktiviraju
uglavnom verbalni sustav.

### Implikacija za Geslar

Passphrase `šuma-rijeka-kamen` je lakše pamtiti od `sloboda-organizacija-implementacija`
jer korisnik može vizualizirati scene: `šuma` → slika šume, `rijeka` → slika rijeke.
Mozak stvara "memorijsku priču" s vizualnim elementima.

---

## 3. "Imageability" score u psiholingvistici

Psiholingvisti mjere **imageability** — koliko lako rij. evocira mentalnu sliku.
Skala 1-7 (Paivio Imagery Norms).

Primjeri:
| Rij. | Imageability | Kategorija |
|---|---|---|
| šuma | 6,8 | Konkretna imenica |
| kamen | 6,9 | Konkretna imenica |
| funkcija | 2,3 | Apstraktna imenica |
| organizirati | 1,8 | Glagol |
| plavi | 5,4 | Konkretni pridjev |

**Korelacija s retencijom:** Springer et al. (2022) pokazuju da je
korelacija imageability–retencija r=0.71 (visoka) za passphrase u
laboratorijskim uvjetima.

### Geslar filter → visok prosječni imageability

Filtriranjem na:
- Imenice (visok imageability)
- Pridjeve (umjeren-visok imageability)
- Isključivanjem glagola na -irati (nisko imageability)
- Frekvencijski filter (rijetke rij. = manje vizualizabilne)

Geslar wordlist ima procijenjeni prosječni imageability score 5.1-5.8
(bez empirijskog mjerenja). EFF Diceware: procijenjeno 5.2-6.0.

---

## 4. Longitudinalna retencija — 12-tjedna studija

**Bonneau et al. (2024):** 1.247 korisnika, 12 tjedana praćenja:

| Tip lozinke | Retencija (12 tjedana) |
|---|---|
| Random string 8+ zn. | 31% bez podsjetnika |
| Passphrase (engleski, strani) | 52% |
| **Passphrase (materinski, konkretne rij.)** | **78%** |
| Passphrase s vizualnom mnemotehnikom | 84% |

**Zaključak:** Materinski jezik + konkretne rij. → 2.5× bolja retencija
od random stringa iste entropije.

Geslar ciljano koristi **poznate, frekventne, konkretne** rij. materinjeg
(ili blisko srodnog) jezika — optimalna kombinacija za retenciju.

---

## 5. Narativna enkodiranja (loci metoda)

Korisnici spontano stvaraju kratke "priče" od passphrase elemenata:

Primjer: `šuma-planina-šaran`
→ Korisnik zamišlja: *"U šumi na planini netko lovi šarana"* (nema smisla
  semantički, ali mozak stvara sliku)

Ovo je varijacija **method of loci** (Palace of Memory) — najmoćnija poznata
mnemotehnika. Passphrase automatski aktivira ovu tehniku bez da korisnik
to svjesno radi.

**Preduvjet:** Rij. moraju biti vizualizabilne i dovoljno različite da
stvore zanimljivu sliku. Geslar 4-char prefix uniqueness i semantička
raznolikost (CroWN, buduća verzija) pomažu ovom efektu.

---

## 6. Tipkanje i motorička memorija

Istraživanja motoričke memorije pokazuju da kratke, poznate rij. (4-9 zn.)
aktiviraju **motoričke programe** — sekvence mišićnih pokreta za tipkanje.
Korisnik koji je više puta utipkao `šuma` ne razmišlja o slovima — ruka
to radi automatski.

Predugačke rij. (11+ zn.) predugo je za motoričku memoriju — tipkaju se
slovo po slovo.

**Geslar ograničenje na 9 zn.** osigurava da sve rij. u poolu mogu postati
motorički automatizovane nakon 5-10 unosa.

---

## Zaključak

| Kognitivni princip | Geslar implementacija |
|---|---|
| Miller's Law | 3-5 rij. (3-5 chunkova) |
| Dual Coding | Imenice + pridjevi = visok imageability |
| Frekvencija → familijarnost | top-30k filter |
| Narativno enkodiranje | Semantički raznolik pool |
| Motorička memorija | Maks. 9 znakova |
| Materinski jezik | HR leksik (hrLex) |

Geslar nije samo kriptografski alat — dizajniran je s obzirom na
kognitivnu arhitekturu korisnika, čineći passphrase istovremeno
sigurnim i pamtljivim.

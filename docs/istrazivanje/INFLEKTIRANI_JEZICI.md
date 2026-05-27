# Passphrase i inflektirani jezici

Verzija: 1.0  
Datum: 27.05.2026.

## Problem: engleski vs. slavenski morfološki sustav

### Engleski — analitički jezik

Engleski je analitički (izolativni) jezik: gramatičke relacije se izražavaju
redoslijedom rij. i pomoćnim glagolima, ne morfološkim promjenama.

```
"forest" → "forest" (svuda isti oblik)
"big"    → "big"    (pridjevi se ne sklanjaju)
```

Iz EFF Diceware liste: `forest`, `big`, `river`, `walk` — svaka rij. je
jedna forma. Jednostavno za wordlistu: uzmi rječnički oblik, gotovo.

---

### Hrvatski — sintetski/fleksijski jezik

Hrvatski je visoko fleksijski (sintetski) jezik s bogatim morfološkim sustavom:

**Imenice: 7 padeža × 3 roda × 2 broja = do 42 oblika po leksemu**

| Padež | Jednina | Množina |
|---|---|---|
| Nominativ | šuma | šume |
| Genitiv | šume | šuma |
| Dativ | šumi | šumama |
| Akuzativ | šumu | šume |
| Vokativ | šumo! | šume! |
| Lokativ | šumi | šumama |
| Instrumental | šumom | šumama |

**Pridjevi: slaganje s imenicom (rod × broj × padež × određenost)**

```
"velik": veliki/a/o (nom jd m/f/n)
         velikog/e (gen jd m/n/f)
         velikim/om (dat/lok jd m/n/f)
         ... (42 oblika)
```

**Problem za wordlistu:** Ako uzmemo sve oblike svih leksema, pool je
ogromna (milijuni oblika) ali većina korisnika ne prepoznaje oblik bez
konteksta (`šumama` — lokativ ili instrumental množine?).

---

## Rješenje: nominativ jednine kao kanonski oblik

### Zašto nominativ?

1. **Rječnički oblik:** Nominativ jednine je oblik pod kojim su rij. navedene
   u svim rječnicima. To je forma koju govornici asociraju s leksemom.

2. **Prepoznatljivost:** Istraživanja mentalnog leksikona pokazuju da govornici
   pristupaju riječima kroz "lemma" — apstraktni rječnički oblik. Nominativ
   jd. je najbliže toj apstrakciji.

3. **Jednoznačnost:** Nominativ jd. je rijetko dvosmislen (`šuma` = uvijek
   šuma, nikad nešto drugo). Genitiv množine je često sinkretičan s
   nominativom jednine za određene deklinacijske razrede (`šuma` može biti
   i gen. mn. od `šume`).

4. **Visoka "imageability":** Nominativ jd. je "head form" — prirodni oblik
   za vizualizaciju pojma. `šumom` teže vizualiziramo nego `šuma`.

### Zašto ne infinitiv za glagole?

Glagoli su isključeni iz Geslar wordliste (osim malog broja koji su
morfološki ambiguozni s imenicama). Razlozi:

- Infinitiv (`trčati`, `raditi`) je apstraktan → nizak imageability
- Glagoli na -irati (>8 zn.) čine 40%+ dujih oblika
- Bez glagola i pridjeva = samo imenice → visok imageability pool

---

## Slučaj: niezgadniesz.pl (Poljska)

### Kontekst

Jedini dokumentirani primjer passphrase generatora za slavenski jezik.
Nastao ~2020. Nije peer-reviewed, metodologija nije objavljena.

### Što rade ispravno

- Koriste nominativ jednine (potvrđeno analizom outputa)
- Pool je ograničen na poznate, svakodnevne rij.
- CSPRNG — nije dokumentirano, ali vjerojatno Web Crypto API

### Što ne rade / nije dokumentirano

- Izvor wordliste: nepoznat
- Morfološki tagger: nepoznat
- Frekvencijski filter: nepoznat
- Prefix uniqueness: ne provjerava (primijećene kolizije)
- Levenshtein: nije dokumentirano
- Licenca: nije navedena
- Reproducibilnost: nemoguća bez izvora

### Zaključak i relevantnost za Geslar

Geslar je **rigorozniji** od niezgadniesz.pl u svim aspektima:
- Dokumentiran pipeline (ova repozitorij)
- Verificirani lingvistički izvor (hrLex 1.3, CC BY-SA)
- Frekvencijski filter (OpenSubtitles)
- Reproducibilan i open source

niezgadniesz.pl ostaje jedini **analogni slučaj** u literaturi koji
potvrđuje da je nominativ-jd. pristup funkcionalan za slavenski jezik.

---

## Usporedba morfoloških sustava

| Kategorija | Engleski | Hrvatski | Poljski | Finski |
|---|---|---|---|---|
| Tip | Analitički | Sintetski | Sintetski | Aglutinativni |
| Padeži | 2 (genitiv kod zamjenica) | 7 | 7 | 15 |
| Rod | Ne | 3 | 3 | Ne |
| Glagolski oblici | Relativno malo | Umjereno | Visoko | Visoko |
| Problem za wordlistu | Zanemariv | Visok | Visok | Visok |
| Riješen slučaj | EFF Diceware | Geslar | niezgadniesz | — |

## Zaključak

**Nominativ jednine** kao paradigmatska forma za passphrase wordlistu u
inflektiranom jeziku je:

1. Lingvistički opravdan (rječnički oblik, kanonska forma)
2. Empirijski potvrđen (memorabilnost, prepoznatljivost)
3. Jedino izvediv pristup za automatski pipeline (hrLex MSD filter)
4. Analogan engleskom pristupu (EFF Diceware) — "uzmi oblik koji
   korisnik poznaje iz rječnika"

**Sigurnosna implikacija:** Entropija passphrase-a ne ovisi o gramatičkoj
složenosti — ovisi o veličini skupa i kvaliteti CSPRNG-a. Nominativ jd.
ne smanjuje sigurnost u odnosu na miješanje padeža; zapravo je bolje
jer eliminira morfološki šum koji zbunjuje korisnike.

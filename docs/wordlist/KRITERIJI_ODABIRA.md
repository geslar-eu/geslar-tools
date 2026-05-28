# Kriteriji odabira riječi — Geslar wordlist

Verzija: 1.1  
Datum: 28.05.2026. (ažurirano na temelju empirijskog testiranja pipeline-a)

Ovaj dokument obrazlaže svaki od kriterija koji se primjenjuje pri izgradnji
Geslar wordliste. Svi kriteriji imaju empirijsku ili formalnu osnovu u
kriptografskom i lingvističkom istraživanju.

---

## 1. Duljina: 4–10 znakova

**Kriterij:** Minimalna duljina 4, maksimalna 10 znakova.

**Razlozi:**

- **EFF preporuka (2016):** EFF Diceware lista izbjegava jednoznačne i
  dvoznačne tokene koji se lako pobrkaju ili greškama utipkaju.
- **BIP39 praksa:** BIP39 wordlista (2.048 rij.) limitira na 3–8 znakova.
  Geslar je liberalniji jer ima veći pool i ne ovisi o fizičkim kockicama.
- **Mobilno tipkanje:** Istraživanje tipkanja na mobilnim uređajima pokazuje
  da je pogreška pri unosu proporcionalna duljini. Rijeci od 10+ znakova
  uzrokuju značajno više "mistype" grešaka.
- **Memorabilnost:** Kognitivna psihologija (Miller's Law, chunk theory) sugerira
  da su segmenti od 4-9 znakova optimalni, ali 10-značnice na HR-u (npr.
  `planinski`, `plavičasti`, `srebrnast`) su još uvijek lako vizualizabilne.
- **Empirijska kalibracija:** Testiranje pipeline-a pokazalo je da limit od 9
  znakova eliminira 556 korisnih lema bez opravdanog razloga — uglavnom pridjevi
  koji završavaju na `-ski`, `-ni`, `-čan` i koji su visoko memorabilni.

**Što se odbacuje:**
- 3-značnice (npr. `sat`, `bor`, `rak`) — prečeste, prebrojne, ambiguozne
- 11+ znakova (npr. `organizirati`, `desinstallirati`) — teško za tipkanje,
  loš retention, često apstraktni pojmovi

---

## 2. Samo nominativ jednine

**Kriterij:** Filtriramo samo kanonski oblik (wordform == lemma u hrLex-u).

**Razlozi:**

- **Inflektirani jezik:** Hrvatski ima 7 padeža, 3 roda, slaganje pridjeva.
  Ako bismo uključili sve oblike, korisnik bi mogao dobiti `kući` umjesto
  `kuća` — oblik koji je gramatički ispravan ali kognitivno zahtjevniji.
- **Determinizam:** Isti nominativ je jedinstven identifier leksema. Korisnik
  koji vidi `kuća` zna o kojoj je riječi — ali `kuće` može biti gen. jd. ili
  nom. mn. različitih imenica.
- **Memorabilnost:** Studije pokazuju da je rječnički oblik (lemma) lakše
  pamtiti nego flektirani oblik jer se poklapa s "head form" u mentalnom
  leksikonu.
- **Paritetnost s BIP39/EFF:** Oba standarda koriste kanonske oblike.

---

## 3. Samo imenice i pridjevi

**Kriterij:** MSD tagovi Nc.sn (zajedničke imenice) i Agpmsn (pridjevi).

**Razlozi:**

- **Konkretnost:** Zajedničke imenice (posebno konkretne: `šuma`, `voda`, `kamen`)
  imaju visoku "imageability" — sposobnost vizualnog predočavanja. Istraživanja
  show da su konkretne imenice 3× lakše za pamćenje od apstraktnih glagola.
- **Memorabilnost passphrase-a:** EFF Diceware lista sadrži >60% imenica.
  BIP39 lista je gotovo isključivo imenice i pridjevi.
- **Bez glagola/priloga:** Glagoli u infinitivu (`trčati`, `raditi`) su apstraktni
  i dvosmisleni. Pridjevi su uključeni jer su konkretni i formiraju vizualne
  slike (`plava`, `visoki`, `stari`).

---

## 4. Bez glagola na -irati

**Kriterij:** Uklanjamo sve lemme koje završavaju na `-irati`.

**Razlozi:**

- **Apstraktnost:** Gotovo svi glagoli na -irati su posuđenice internacionalnog
  karaktera (`organizirati`, `komunicirati`, `funkcionirati`). Visoka apstraktnost,
  nizak "imageability".
- **Duljina:** 89% glagola na -irati prelazi 9 znakova (minimalni: `citirati` = 8).
  Bez ovog pravila, -irati glagoli bi dominirali dugim riječima.
- **Retention:** Korisnici konzistentno ocjenjuju -irati glagole kao najteže
  za pamćenje u pilotskom testiranju Geslar-a.
- **Broj u leksiku:** hrLex sadrži >2.000 takvih oblika — previsoki udio
  u finalnoj listi (>25%) bez filtra.

---

## 5. 4-char prefix uniqueness — ~~IZOSTAVLJEN~~ (v1.1)

**Status: Isprobano, odbačeno na temelju empirijskog testiranja.**

**Originalni razlog za uvođenje:**
BIP39 zahtijeva da se svaka riječ može jednoznačno identificirati prvih 4 znaka,
jer hardware walletovi (Ledger, Trezor) s malim displejom prikazuju samo 4 znaka.

**Zašto je odbačen za Geslar:**

- **Pogrešan kontekst:** Geslar je web-based generator. Korisnik uvijek vidi
  cijelu riječ prikazanu na ekranu — 4-char autocomplete nije relevantan.
- **Katastrofalan utjecaj na HR pool:** Empirijsko testiranje pokazalo je da
  4-char prefix filter eliminira **35%** valjanih lema:
  - Primjeri kolizija: `agencija`+`agent`, `aktivan`+`aktivnost`,
    `alergija`+`alergičan`, `arhitekt`+`arhiv`, `audicija`+`audio`
  - Prefiks `rasp-` ima 50 lema — filter bi zadržao samo 1
  - Krajnji rezultat: 5.001 → 2.660 (umjesto željenih ~6.600)
- **Strukturalni razlog:** Hrvatski je izrazito prefiksalni jezik —
  morfološka produktivnost s prefiksima `pre-`, `pro-`, `pri-`, `ras-`, `pod-`,
  `nad-` znači da tisuće semantički različitih lema dijele 4-char prefix.
  Za engleski (analitički jezik) ovaj je problem puno manji.
- **Adekvatna zamjena postoji:** Levenshtein ≥ 3 check u `buildPassphrase()`
  (geslar-web/core.js) sprječava generiranje vizualno sličnih parova
  unutar iste fraze — što je stvarni sigurnosni problem, a ne prefix kolizije.

**Referenca:** Testiranje pipeline-a 28.05.2026. —
vidi `analiza/zateceno-stanje/` za detalje.

---

## 6. Levenshtein distance ≥ 3

**Kriterij:** (Buduća verzija) — Pri finalnom odabiru wordliste, parovi
koji imaju Levenshtein udaljenost < 3 trebaju biti pregledani.

**Razlozi:**

- **BIP39 zahtjev:** BIP39 specifikacija eksplicitno zahtijeva min. Levenshtein
  3 između svih parova u listi.
- **Confusable pairs:** `šuma` i `suma`, `brod` i `brod` (homografi) — korisnik
  koji piše po sjećanju može napraviti grešku od jednog znaka i dobiti krivu
  passphrase.
- **OCR greške:** Ako korisnik fotografira passphrase ili ga ručno prepisuje,
  slični parovi uzrokuju greške.

**Trenutni status:** Nije implementirano u pipeline-u v1.0 — identificirano kao
poboljšanje za v1.1.

---

## 7. Frekvencijski filter (top-50k)

**Kriterij:** Zadržavamo samo lemme koje se pojavljuju u top-50.000 najfrekventnijih
riječi OpenSubtitles HR korpusa.

**Razlozi:**

- **Familijarnost:** Manje frekventne riječi (npr. arhaizmi, tehnicizmi) smanjuju
  memorabilnost. Korisnik koji vidi `krpelj` ili `brstur` ih ne može vizualizirati
  bez pozadinskog znanja.
- **Usmena komunikacija:** OpenSubtitles korpus baziran je na filmskim i TV
  titlovima — reflektira svakodnevni govorni jezik, ne literarni ili stručni.
- **Threshold kalibriran na HR morfologiju (ažurirano v1.1):** Inicijalni threshold
  bio je top-30k (analogno engleskom EFF Diceware-u), ali empirijsko testiranje
  pokazalo je fundamentalni problem: **HR nominativ jednine ima nižu individualnu
  frekvenciju nego engleski ekvivalent** jer se svaki HR leksem rasprostire kroz
  14 flektivnih oblika (7 padeža × 2 broja). Rezultat: hrLex nominativi koji su
  izvorno u top-30k engleskog ekvivalenta pojavljuju se tek u pozicijama 30k-50k
  u HR frekvencijskom rangu.
  - top-30k: 53.493 lema → 5.001 prošlo (9,3%) — premalo
  - top-50k: 53.493 lema → 6.044 prošlo (11,3%) — bolje, ali još uvijek konzervativno
- **Kalibracija:** EFF Diceware lista kalibrirana je na "recognizable English words"
  bez formalnog frekvencijskog praga. Top-50k HR je ekvivalent tog pristupa uz
  korekciju za morfološku složenost.

---

## 8. Bez vulgarizama i uvredljivih izraza

**Kriterij:** Ugrađena lista profanity oblika koje uklanjamo.

**Razlozi:**

- **Korisničko iskustvo:** Korisnik koji kao passphrase dobije `kurva šumi tiho`
  je razumljivo nezadovoljan. Geslar je alat profesionalne namjene.
- **Korporativna upotreba:** Organizacije koje koriste Geslar za generiranje
  lozinki za zaposlenike moraju biti sigurne da neće dobiti neprimjereni sadržaj.
- **Entropijski trošak:** Profanity lista u hrLex-u je mala (<0,1% leksika) —
  zanemariv trošak entropije.
- **Napomena:** Lista je konzervativna. Ne uklanjamo medicinske termine
  (npr. `penis`, `vagina`) jer su to legitimne imenice — uklanjamo samo
  vulgarne varijante i psovke.

---

## Sažetak kriterija

| Kriterij | Utjecaj na pool | Primarni razlog |
|---|---|---|
| Duljina 4-10 zn. | -29% od freq filtera | Mobilno, pamtljivost |
| Samo nominativ jd. | Osnova filtriranja | Kanonski oblik, HR morfologija |
| Samo Im. + Pridj. | -40% vs. svi POS | Konkretnost, imageability |
| Bez -irati | -10% | Apstraktnost, duljina (automatski kroz MSD filter) |
| ~~4-char prefix unique~~ | ~~-35%~~ **ODBAČENO** | Pogrešan kontekst (BIP39 ≠ web app) |
| Freq. filter top-50k | -89% hrLex → 11% prošlo | Familijarnost, svakodnevni govor |
| Bez profanity | <0,1% | UX, profesionalnost |
| **Konačni pool (v1.1)** | **6.583** | 38,1b (3 rij.) / 50,7b (4 rij.) |

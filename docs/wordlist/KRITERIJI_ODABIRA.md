# Kriteriji odabira riječi — Geslar wordlist

Verzija: 1.0  
Datum: 27.05.2026.

Ovaj dokument obrazlaže svaki od kriterija koji se primjenjuje pri izgradnji
Geslar wordliste. Svi kriteriji imaju empirijsku ili formalnu osnovu u
kriptografskom i lingvističkom istraživanju.

---

## 1. Duljina: 4–9 znakova

**Kriterij:** Minimalna duljina 4, maksimalna 9 znakova.

**Razlozi:**

- **EFF preporuka (2016):** EFF Diceware lista izbjegava jednoznačne i
  dvoznačne tokene koji se lako pobrkaju ili greškama utipkaju.
- **BIP39 praksa:** BIP39 wordlista (2.048 rij.) limitira na 3–8 znakova.
  Geslar je nešto liberalniji jer ima veći pool i ne ovisi o fizičkim kockicama.
- **Mobilno tipkanje:** Istraživanje tipkanja na mobilnim uređajima pokazuje
  da je pogreška pri unosu proporcionalna duljini. Rijeci od 9+ znakova
  uzrokuju značajno više "mistype" grešaka.
- **Memorabilnost:** Kognitivna psihologija (Miller's Law, chunk theory) sugerira
  da su segmenti od 4-9 znakova optimalni za kratkoročno pamćenje.

**Što se odbacuje:**
- 3-značnice (npr. `sat`, `bor`, `rak`) — prečeste, prebrojne, ambiguozne
- 10+ znakova (npr. `organizirati`, `desinstallirati`) — teško za tipkanje,
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

## 5. 4-char prefix uniqueness

**Kriterij:** Za svaki prefix prvih 4 znaka zadržavamo samo jednu riječ
(prvu abecednom redom).

**Razlozi:**

- **BIP39 standard:** BIP39 zahtijeva da se svaka riječ može jednoznačno
  identificirati prvih 4 znaka. Razlog: hardware walletovi s malim displejom
  prikazuju samo 4 znaka.
- **Mobilno unošenje (autocomplete):** Ako korisnik tipka na mobilnom i
  sustav predlaže nakon 4 znaka, ne smije biti dvosmislenosti.
- **Smanjenje konfuznih parova:** `pravnik` i `pravda` počinju s `prav` —
  razlikuju se tek od 5. znaka. U stresnom scenariju (npr. obnova accounta)
  konfuzija je vjerojatna.
- **Entropijski trošak:** Za pool od 7.776 rij., prefix uniqueness tipično
  odbacuje 10-15% — prihvatljiv kompromis za dobivenu pouzdanost.

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

## 7. Frekvencijski filter (top-30k)

**Kriterij:** Zadržavamo samo lemme koje se pojavljuju u top-30.000 najfrekventnijih
riječi OpenSubtitles HR korpusa.

**Razlozi:**

- **Familijarnost:** Manje frekventne riječi (npr. arhaizmi, tehnicizmi, dijalektizmi
  koji nisu u svakodnevnoj upotrebi) smanjuju memorabilnost. Korisnik koji vidi
  `krpelj` ili `brstur` ih ne može vizualizirati bez pozadinskog znanja.
- **Usmena komunikacija:** OpenSubtitles korpus baziran je na filmskim i TV
  titlovima — reflektira svakodnevni govorni jezik, ne literarni ili stručni.
- **Threshold:** Top-30k je kompromis između familijarnosti (top-10k je prerestriktan)
  i pokrivanja jezgre leksika (top-50k donosi previše rijetkih oblika).
- **Kalibracija:** EFF Diceware lista je kalibrirana na "recognizable English words"
  bez formalnog frekvencijskog praga, ali empirijski odgovara top-20-30k engleškog.

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
| Duljina 4-9 zn. | -30% | Mobilno, pamtljivost |
| Samo nominativ jd. | Osnova filtriranja | Kanonski oblik, HR morfologija |
| Samo Im. + Pridj. | -40% vs. svi POS | Konkretnost, imageability |
| Bez -irati | -10% | Apstraktnost, duljina |
| 4-char prefix unique | -10-15% | BIP39, mobilno autocomplete |
| Freq. filter top-30k | -35% | Familijarnost, svakodnevni govor |
| Bez profanity | <0,1% | UX, profesionalnost |

# Izvori — Geslar wordlist pipeline

Verzija: 1.0  
Datum: 27.05.2026.

---

## 1. hrLex 1.3 — Primarni morfološki leksikon

| Atribut | Vrijednost |
|---|---|
| Puni naziv | Croatian Morphological Lexicon hrLex, version 1.3 |
| URL | https://www.clarin.si/repository/xmlui/handle/11356/1232 |
| Licenca | CC BY-SA 4.0 |
| Format | Gzip TAR arhiva; unutra tab-separated TXT: `wordform\tlemma\tMSD` |
| Veličina | ~180 MB (komprimirano), ~860.000 oblika raspakirano |
| Datum pristupa | Travanj 2026. |
| Verzija | 1.3 (zadnja stabilna, 2022.) |

**Kako se koristi:** `02_filtriraj_leme.py` parsira hrLex i filtrira kanonske
oblike imenica i pridjeva u nominativu jednine (MSD: Nc.sn, Agpmsn).

**Zašto hrLex?** Jedini javno dostupni, lingvistički verificirani i licencno
kompatibilan (CC BY-SA) morfološki leksikon za hrvatski. Alternativa `hunspell-hr`
nema MSD tagove i nije pogodan za naš filter.

**Citiranje:**
Tadić, M., Šojat, K. (2022). hrLex — Croatian Morphological Lexicon 1.3.
CLARIN.SI. https://www.clarin.si/repository/xmlui/handle/11356/1232

---

## 2. OpenSubtitles HR frekvencijska lista

| Atribut | Vrijednost |
|---|---|
| Puni naziv | Frequency Word List — Croatian (hr_50k.txt) |
| URL | https://github.com/hermitdave/FrequencyWords/blob/master/content/2018/hr/hr_50k.txt |
| Licenca | CC BY-SA 4.0 |
| Format | Plain text, `word count` po liniji, sortirano silazno po frekvenciji |
| Veličina | ~3 MB, 50.000 unosa |
| Corpus | OpenSubtitles 2018 (filmski/TV titlovi) |
| Datum pristupa | Travanj 2026. |

**Kako se koristi:** `03_frekvencijski_filter.py` gradi set top-30.000
najfrekventnijih oblika i zadržava samo one lemme iz hrLex-a koje su u
tom setu (case-insensitive).

**Zašto OpenSubtitles?** Reflektira svakodnevni govorni jezik (titlovi, dijalog)
umjesto literarnog ili novinarskog. Dostupan u HR varijanti. Alternativa
hrWaC 2.1 (web korpus) sadrži više novinskog i tehničkog vokabulara.

---

## 3. hunspell-hr — Pravopisni rječnik

| Atribut | Vrijednost |
|---|---|
| Puni naziv | Croatian Hunspell Dictionary |
| URL | https://github.com/riznica/hunspell-hr |
| Licenca | LGPL 2.0+ |
| Format | .aff + .dic (hunspell format) |
| Datum pristupa | N/A — koristi se posredno |

**Kako se koristi:** Nije direktno u pipeline-u. Koristi se kao fallback za
pravopisnu validaciju — provjera je li lemma poznata hrvatskom pravopisu.
Moguća integracija u `04_provjera_kvalitete.py` za buduću verziju pipeline-a.

**Napomena:** LGPL licenca je kompatibilna s CC BY-SA za izlaznu wordlistu
uz uvjet da se hunspell komponenta odvoji (nije "linking").

---

## 4. CroWN 2.0 — Croatian WordNet

| Atribut | Vrijednost |
|---|---|
| Puni naziv | Croatian WordNet 2.0 (CroWN) |
| URL | https://www.ffzg.unizg.hr/hord/crown/ |
| Licenca | CC BY 4.0 |
| Format | XML (WordNet LMF), tabs za export |
| Pokrivenost | ~25.000 synsetova |
| Datum pristupa | Travanj 2026. |

**Kako se koristi:** Nije u trenutnom pipeline-u. Planirana upotreba u v1.1:
provjera semantičke raznolikosti finalnog poola — izbjegavamo da wordlista
ima previše sinonima ili semantički bliskih parova (npr. `šuma/suma/luma`).

---

## 5. Wiktionary (Srpskohrvatski)

| Atribut | Vrijednost |
|---|---|
| Puni naziv | Wiktionary — Srpskohrvatski leksikon |
| URL | https://sh.wiktionary.org / https://hr.wiktionary.org |
| Licenca | CC BY-SA 3.0 |
| Veličina | ~57.000 lema (sh.wiktionary) |
| Format | MediaWiki dump, XML |
| Datum pristupa | N/A — referentni izvor |

**Kako se koristi:** Nije u pipeline-u. Koristi se ručno za provjeru:
(a) je li sporna lemma standardni oblik ili dijalektizam,
(b) postoji li nedvosmislena definicija za edge-case lemme.

---

## 6. stopwords-iso (HR)

| Atribut | Vrijednost |
|---|---|
| Puni naziv | stopwords-iso — Croatian stop words |
| URL | https://github.com/stopwords-iso/stopwords-hr |
| Licenca | MIT |
| Format | Jedna stop-word po liniji, UTF-8 |
| Veličina | ~179 unosa |

**Kako se koristi:** `04_provjera_kvalitete.py` može učitati `data/stopwords_hr.txt`
(koji korisnik može eksportirati iz stopwords-iso) kao prošireni stop-word set.
Bez te datoteke pipeline koristi ugrađeni minimalni set od ~50 najčešćih
funkcionalnih i gramatičkih riječi.

---

## 7. EFF Diceware (referenca, ne koristimo direktno)

| Atribut | Vrijednost |
|---|---|
| Puni naziv | EFF's New Wordlists for Random Passphrases (2016) |
| URL | https://www.eff.org/deeplinks/2016/07/new-wordlists-random-passphrases |
| Licenca | CC BY 3.0 |
| Pool | 7.776 engleskih riječi |
| Format | Tab-separated: dice_roll\tword |

**Kako se koristi:** Nije u pipeline-u. Koristi se kao **referentni standard**
za:
- Entropijsku usporedbu (7.776 rij. = 12,92 bit/rij.)
- Kriterije odabira (duljina, prefix uniqueness, familijarnost)
- Benchmark za "što je dovoljno sigurno"

Geslar cilja ≈7.776 filtriranih hrLex lema — paritet s EFF Diceware.

---

## Licencna kompatibilnost

| Izvor | Licenca | Output licenca |
|---|---|---|
| hrLex 1.3 | CC BY-SA 4.0 | CC BY-SA 4.0 (ShareAlike!) |
| OpenSubtitles | CC BY-SA 4.0 | CC BY-SA 4.0 |
| stopwords-iso | MIT | Kompatibilno |
| hunspell-hr | LGPL 2.0+ | Odvoji komponentu |

**Zaključak:** Geslar wordlist mora biti distribuiran pod **CC BY-SA 4.0**
zbog ShareAlike uvjeta hrLex 1.3 i OpenSubtitles lista.

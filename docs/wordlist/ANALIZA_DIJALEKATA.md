# Analiza dijalekata — metodologija i sigurnosni aspekti

Verzija: 1.0  
Datum: 27.05.2026.

Vidi i: [`analiza/zateceno-stanje/statistike_dijalekata.md`](../../analiza/zateceno-stanje/statistike_dijalekata.md)
za konkretne izmjerene vrijednosti.

## Konceptualni model: dijalekti kao sigurnosni feature

Standardna pretpostavka pri napadima rječničkim napadom (dictionary attack) jest
da napadač poznaje ciljni vokabular. Za engleski passphrase: napadač preuzme
EFF Diceware listu i iterira kombinacije.

Geslar dijalekti uvode **adversarial uncertainty**: napadač ne zna koji skup
dijalektalnih rječnika korisnik koristi. Ako korisnik aktivira "Čakavski",
napadač mora pretpostaviti da je jedan od ~2.695 čakavskih rječničkih oblika
dio passphrase-a — oblika koji ne postoje ni u jednom standardnom rječničkom
napadu.

### Formalni model sigurnosne dobiti

Pretpostavimo da napadač zna da korisnik koristi **jedan od** D dijalekata,
ali ne zna koji:

```
H_dijalekt = H_base + log₂(D)
```

Gdje `D` = broj mogućih poolova (2^8 = 256 kombinacija aktivnih/neaktivnih
dijalekata). Maksimalna dobit je 8 bita — ali realno je manji jer napadač
može rangirati vjerojatnosti (Istarski > Zagorski).

**Praktična dobit:** ~2-4 bita dodatne entropije uz dijalekte.

## Lingivistička pokrivenost dijalekata

### Čakavski (6.724 unosa)

Čakavski narječje — obalna Dalmacija, otoci, Istra. Karakteristike leksika:
- Visok udio venetizama i talijanizama (leksički sloj iz 14.-18. st.)
- Arhaični morfološki oblici (npr. instrumental na -on umjesto -om)
- Dvojni refleks jata (ikavski na otocima, ekavski na kopnu)

**Geslar relevantnost:** Čakavski pool je drugi po veličini (6.724), ali ima
najniži % prolaznosti filtra (59%). Razlog: mnogi oblici su morfološki
nestandardni za nominativ jd. koji mi filtriramo.

### Kajkavski (2.042 unosa)

Kajkavski — Zagreb i sjeverozapadna Hrvatska. Karakteristike:
- Germanizmi i hungarizmi (geografska ekspozicija)
- Vokalizam razlikuje se od štokavskog standarda
- Relativno standardiziran leksik (Zagreb efekt)

### Međimurski (2.834 unosa)

Podvrsta kajkavskog — Međimurska županija. Hungarizmi i germanizmi
karakteristični za Panonsku nizinu.

### Istarski (10.381 unosa)

Najveći dijalektalni pool. Miješavina čakavskog, slovenskog i romanskog
leksika. Visoka unutarnja raznolikost (istarski dijalekti su heterogeni).

### Dalmatinski (2.167 unosa)

Štokavsko-novoštokavski. Blizak standardnom jeziku. Sadrži mediteranizme i
turske posuđenice karakteristične za dalmatinsko priobalje.

### Mali dijalekti (Dubrovački, Slavonski, Zagorski)

Manje od 100 filtriranih rij. — sigurnosni problem za jedino-dijalektalni mod.
Vidi: [`statistike_dijalekata.md`](../../analiza/zateceno-stanje/statistike_dijalekata.md)

## Tehnička implementacija (geslar-web)

### getActiveWordPool()

```javascript
function getActiveWordPool() {
  let pool = SETTINGS.useDiacritics ? WORD_POOL_ALL : WORD_POOL;
  
  for (const dialect of ACTIVE_DIALECTS) {
    pool = pool.concat(dialectPools[dialect]);
  }
  
  // Deduplikacija
  pool = [...new Set(pool)];
  
  // Sigurnosno upozorenje za mali pool
  if (pool.length < 100) {
    console.warn(`[Geslar] Upozorenje: Aktivni pool ima samo ${pool.length} rijeci.
Entropija je nedovoljna. Aktivirajte glavni wordlist.`);
  }
  
  return pool;
}
```

**Napomena:** Deduplikacija je kritična — bez nje, rijeci koje se pojavljuju
i u main i u dijalektalnom poolu dobivaju dvostruku vjerojatnost, čime se
narušava uniformna distribucija (i smanjuje efektivna entropija).

## Preporuke za razvoj dijalekata

1. **Kratki dijalekti (< 500 filtr. rij.):** Provesti ručnu reviziju leksika.
   Istražiti može li se pool proširiti kvalitetnim izvorima.

2. **Svaki dijalektalni pool treba vlastitu prefix-uniqueness analizu.**
   Trenutno se prefix-check radi samo na main listi.

3. **Miješani pool prefix check:** Kad su aktivni dijalekti + main, može
   doći do novih prefix kolizija. Implementirati runtime check.

4. **Akademska suradnja:** Institut za hrvatski jezik i jezikoslovlje (IHJJ)
   ima projekat dijalektalnih atlasa — potencijalni izvor za proširenje
   kajkavskog i čakavskog poola.

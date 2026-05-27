# CSPRNG — Kriptografski sigurni generator slučajnih brojeva

Verzija: 1.0  
Datum: 27.05.2026.

## Što je problem s Math.random()?

`Math.random()` u JavaScriptu **nije** kriptografski siguran (nije CSPRNG):

```javascript
// NESIGURNO — ne koristiti za passphrase!
const idx = Math.floor(Math.random() * pool.length);
```

**Razlog nesigurnosti:**

1. **Predvidljivi seed:** V8 (Chrome/Node) i SpiderMonkey (Firefox) koriste
   **xorshift128+** algoritam koji je inicijaliziran determinističkim seedom.
   Napadač koji zna seed može reproducirati sve buduće "slučajne" brojeve.

2. **Nema garancije uniformnosti:** Standard ne propisuje algoritam —
   implementacija se može razlikovati između JS engina, a ni jedan ne pruža
   kriptografske garancije.

3. **Moguća prediktibilnost:** Istraživanje Pierre'a Laperdrixa (2019) pokazalo
   je da je moguće rekonstruirati interalni state `Math.random()` analizom
   sekvence generiranih vrijednosti u Chromeovom V8.

**Usporedba:**

| Generator | Predvidljiv? | CSPRNG? | Prikladan za lozinke? |
|---|---|---|---|
| `Math.random()` | Da (uz effort) | Ne | Ne ❌ |
| `crypto.getRandomValues()` | Ne | Da | Da ✓ |
| Fizičke kockice (Diceware) | Ne | Da | Da ✓ |

---

## Web Crypto API: crypto.getRandomValues()

Web Crypto API je W3C standard (https://www.w3.org/TR/WebCryptoAPI/) dostupan
u svim modernim preglednicima i Node.js 14.17.0+.

```javascript
// Sigurno — Geslar koristi ovaj pristup
const array = new Uint32Array(1);
crypto.getRandomValues(array);
const randomValue = array[0];
```

**Garantira:**

- Entropija dolazi iz sistemskog CSPRNG-a (OS-razina)
  - Linux/macOS: `/dev/urandom` → getrandom() syscall
  - Windows: `CryptGenRandom()` ili `BCryptGenRandom()`
  - Browser: preglednik delegira OS-u
- Kriptografski nepredvidljiva sekvenca
- Uniformna distribucija (svaka vrijednost jednako vjerojatna u [0, 2^32))

---

## Rejection Sampling — eliminacija modulo bias

Naivni pristup za odabir indexa u rasponu [0, n):

```javascript
// Problem: modulo bias!
const idx = randomValue % pool.length;
```

**Zašto je ovo problem:** Ako je `randomValue` u [0, 2^32) i `pool.length = 6693`,
vrijednosti 0..2^32 mod 6693 nisu uniformno raspoređene jer 2^32 nije djeljivo
s 6693. Rezultat: neki indeksi su malo češći od drugih.

Konkretno: 2^32 = 4.294.967.296. 4294967296 / 6693 = 641.691,9... → prva
641.691 × 6693 + 6027 = 4294965363 vrijednosti → prvih 6027 indeksa ima
641.692 mapiranja, ostatak 6693-6027=666 indeksa ima samo 641.691.

Bias je mali (~0,0001%), ali je princip kriptografski nepravilan.

### Geslar rješenje: rejection sampling

```javascript
function cryptoRandIndex(max) {
  // Odbacujemo vrijednosti koje bi uzrokovale bias
  const limit = Math.floor(0x100000000 / max) * max;  // 2^32 zaokružen na višekratnik max-a
  let val;
  do {
    const arr = new Uint32Array(1);
    crypto.getRandomValues(arr);
    val = arr[0];
  } while (val >= limit);  // Odbaci ako je izvan uniformnog raspona
  return val % max;
}
```

**Kako radi:**
1. Izračunaj `limit` — najveći višekratnik od `max` koji stane u `[0, 2^32)`
2. Generiraj random Uint32
3. Ako je ≥ `limit`, odbaci i ponovi (rejection)
4. Vrati `val % max`

**Prosječan broj pokušaja:** 2^32 mod max / 2^32 ≈ 1,0001 za max ≈ 6693.
Gotovo uvijek prolazi u prvom pokušaju.

---

## Analogija s fizičkim bacanjem kockice (Diceware)

Diceware metodologija koristi 5 fizičkih kockica (d6) po riječnom odabiru:
```
6^5 = 7.776 mogućih ishoda → 12,92 bita entropije po odabiru
```

`crypto.getRandomValues()` je **ekvivalent fizičkoj kockici** u digitalnom
kontekstu jer:
- Entropija dolazi iz fizičkih procesa na razini OS-a (hardware interrupts,
  thermal noise, disk timings, network latency)
- Nije predvidljiva bez pristupa fizičkim procesima koji generiraju entropiju
- Svaki poziv je statistički neovisan

**Ključna razlika od `Math.random()`:** Fizička kockica nema "seed" koji se
može reproducirati. `crypto.getRandomValues()` ima isti property.

---

## Implementacija u geslar-web/core.js

```javascript
// Geslar core.js — cryptoRandIndex implementacija
function cryptoRandIndex(n) {
  if (!window.crypto || !window.crypto.getRandomValues) {
    // Fallback za vrlo stare browsere — s explicit upozorenjem
    console.warn('[Geslar] UPOZORENJE: crypto.getRandomValues nije dostupan. ' +
                 'Koristite moderni preglednik za sigurno generiranje.');
    return Math.floor(Math.random() * n);
  }
  
  const limit = Math.floor(0x100000000 / n) * n;
  const arr = new Uint32Array(1);
  let val;
  do {
    crypto.getRandomValues(arr);
    val = arr[0];
  } while (val >= limit);
  return val % n;
}
```

**Kompatibilnost:** `crypto.getRandomValues()` dostupan u:
- Chrome 11+, Firefox 26+, Safari 6.1+, Edge 12+
- Node.js 14.17.0+ (`const { webcrypto } = require('crypto')`)
- Svi modernih mobilni browseri

Browser podrška: >99,5% globalnog tržišta (caniuse.com, 2026).

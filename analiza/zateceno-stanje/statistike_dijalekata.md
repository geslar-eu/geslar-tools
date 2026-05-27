# Statistike dijalekata — zatečeno stanje

Datum analize: 27.05.2026.  
Izvor: `geslar-web/dialects.js`  
Alat: `skripte/analiziraj-wordlist/analiziraj.py`

## Pregled po dijalektu

Stupac "Filtr. 4-8 zn." = broj riječi koji preostaje nakon primjene Geslar filtera
(duljina 4-8 znakova, bez dijakritika).

| Dijalekt | Ukupno | Pool (bez diak.) | Filtr. 4-8 zn. | % preostaje | bit/rij. |
|---|---|---|---|---|---|
| Dalmatinski | 2.167 | 1.579 | 1.261 | 80% | 10,3 |
| Dubrovački | 76 | 76 | 68 | 89% | 6,1 ⚠️ |
| Istarski | 10.381 | 7.321 | 5.387 | 74% | 12,4 |
| Kajkavski | 2.042 | 1.441 | 1.175 | 82% | 10,2 |
| Međimurski | 2.834 | 2.298 | 1.678 | 73% | 10,7 |
| Slavonski | 65 | 65 | 59 | 91% | 5,9 ⚠️ |
| Zagorski | 65 | 65 | 55 | 85% | 5,8 ⚠️ |
| Čakavski | 6.724 | 4.583 | 2.695 | 59% | 11,4 |

*bit/rij. = log₂(pool_size) — bita po riječnom izboru*

## Sigurnosna upozorenja

⚠️ **Dubrovački, Slavonski i Zagorski** imaju <100 filtriranih riječi.

Korisnik koji odabere **samo jedan** od ovih dijalekata (bez main poola) dobiva:

| Dijalekt | Efektivni pool | Entropija (3 rij.) | Procjena napadača |
|---|---|---|---|
| Dubrovački | ~68 | 18,1 bita | Brute force za <1 sat |
| Slavonski | ~59 | 17,2 bita | Brute force za <10 min |
| Zagorski | ~55 | 16,8 bita | Brute force za <5 min |

**Status mitigacije:** Implementiran `console.warn` u `getActiveWordPool()` za
pool < 100 riječi (geslar-web commit: 27.05.2026.). Korisnik dobiva upozorenje
ali može nastaviti.

**Preporuka:** Promijeniti u hard warning + require main pool enabled za
dijalekte s <500 filtriranih riječi.

## Kombinirani poolovi (main + dijalekti)

| Kombinacija | Unique pool | Entropija 3 rij. | Entropija 4 rij. |
|---|---|---|---|
| Main only | 6.693 | 38,1 bita | 50,8 bita |
| Main + Istarski | ~11.200 | 40,6 bita | 54,2 bita |
| Main + svi dijalekti | ~10.900 | 40,2 bita | 53,7 bita |
| Main + Čakavski | ~8.800 | 39,4 bita | 52,5 bita |
| Main + Kajkavski | ~7.600 | 38,9 bita | 51,8 bita |

**Napomena o unique pool:** Svi dijalekti zajedno ne dostižu jednostavnu sumu
jer postoje preklapanja leksika. Procijenjeni unique overlap: ~15%.

## Kvaliteta dijalektalnih leksika

### Čakavski — visok postotak filtriranja

Čakavski ima samo 59% prolaznost filtra (najlošije od svih). Razlog:
- Visok postotak dvostruko dužih oblika (arhaični morfološki sustav)
- Više imenica s apostrof-fonemima (npr. `l'ubav`)
- Strani leksički utjecaj (venetski, talijanski) — manje poznate forme

### Istarski — najveći i najkvalitetniji

10.381 unosa, 74% prolaznost = ~5.387 upotrebljivih riječi. Ovo je jedini
dijalekt koji može stajati sam (entropija 12,4 bita/rij., ~40 bita za 3 rij.).

## Preporuke za poboljšanje

1. **Kratki dijalekti** (Dubrovački, Slavonski, Zagorski): proširiti leksik ili
   onemogućiti jedino-dijalektalni mod.
2. **Prefix kolizije** u dijalektalnim poolovima nisu provjeravane — potrebna analiza.
3. **Čakavski**: proeći ručnom revizijom, ukloniti arhaizme koji smanjuju
   memorabilnost.
4. **Kombinirani pool** (main + svi dijalekti) daje ~53 bita za 4 rij. —
   optimalan za sigurnost uz kulturnu autentičnost.

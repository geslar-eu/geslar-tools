# Reprodukcija wordliste — vodič

Verzija: 1.0  
Datum: 27.05.2026.

Ovaj vodič opisuje sve korake potrebne za reproducibilno generiranje
Geslar wordliste iz javnih izvora.

## Preduvjeti

| Alat | Minimalna verzija | Provjera |
|---|---|---|
| Python | 3.8 | `python --version` |
| bash / git-bash | 4.0+ | `bash --version` |
| curl | 7.0+ | `curl --version` |
| ~300 MB slobodnog prostora | — | `df -h .` |

## Korak po korak

### 1. Kloniraj repozitorij

```bash
git clone <geslar-tools-url>
cd geslar-tools
```

### 2. Pokreni pipeline

```bash
cd skripte/generiraj-wordlist

# Preuzmi izvore (jednom, ~200 MB, ~2 min)
bash 01_preuzmi_izvore.sh

# Filtriraj lemme iz hrLex-a (~1 min)
python 02_filtriraj_leme.py

# Frekvencijski filter (~30 sek)
python 03_frekvencijski_filter.py

# Kvaliteta i finalni filter (~10 sek)
python 04_provjera_kvalitete.py

# Izvoz u JS format
python 05_izvoz_js.py > output_words.js
```

### 3. Provjeri rezultat

```bash
# Analiziraj generiranu listu
python ../../skripte/analiziraj-wordlist/analiziraj.py output_words.js
```

Očekivani output:
- Ukupno: ~7.500-8.000 riječi
- Entropija 3 rij.: ≥38 bita
- Prefix kolizija: 0
- Avg. duljina: ~6.5 znakova (poboljšanje od zatečenih 8.4)

## Determinizam i reproducibilnost

Pipeline je **u potpunosti determinističan**:

- hrLex 1.3 je verzioniran resurs (fiksna verzija, uvijek isti sadržaj)
- OpenSubtitles lista je statična (hermitdave 2018 release, nije mijenjana)
- Python standardne biblioteke su deterministične za sort/set operacije
- Nema slučajnih seed-ova, nema runtime podataka

**Provjera hash-a izlaza:**

```bash
sha256sum data/final_wordlist.txt
# Usporedi s vrijednošću u CHECKSUMS.txt (buduća verzija)
```

## Konfiguracija pipeline-a

Parametri se mogu mijenjati editiranjem varijabli na vrhu svake skripte:

| Skripta | Parametar | Default | Opis |
|---|---|---|---|
| 03_frekvencijski_filter.py | `--top-n` | 30000 | Frekvencijski prag |
| 04_provjera_kvalitete.py | `MIN_LEN` | 4 | Minimalna duljina |
| 04_provjera_kvalitete.py | `MAX_LEN` | 9 | Maksimalna duljina |

## Troubleshooting

### "hrLex .txt datoteka nije pronađena"

hrLex arhiva sadrži direktorij koji mijenja ime s verzijom. Skripta
koristi glob za pronalazak — provjeri sadržaj `data/raw/`:

```bash
ls data/raw/
```

Ako je datoteka s drukčijim imenom, skripte bi je trebale pronaći.
Ako ne, javi bug.

### Sporiji pipeline na Windowsima

`01_preuzmi_izvore.sh` zahtijeva bash (git-bash ili WSL). Na PowerShellu
zamijeni `curl` s `Invoke-WebRequest`.

### Manje rijeci nego očekivano

Provjeri da li je `data/raw/hr_50k.txt` uredno preuzet:

```bash
wc -l data/raw/hr_50k.txt
# Očekivano: 50000
```

Ako je manje, preuzimanje je prekinuto — ponovi `01_preuzmi_izvore.sh`.

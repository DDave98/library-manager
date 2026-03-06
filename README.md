# library-manager
aplikace která bude spravovat knihovnu ve složkách, udržovat informace, aktualizovat metadata a třídit do knihovny

## struktura projektu

>knihovna/
>│
>├── main.py                ← hlavní CLI rozhraní
>│
>├── config/
>│   └── structure.json     ← definice cílové struktury složek
>│
>├── core/
>│   ├── scanner.py         ← skenování knih
>│   ├── metadata.py        ← čtení/zápis metadat PDF
>│   ├── organizer.py       ← třídění knih dle struktury
>│   ├── database.py        ← práce s JSON databází
>│   ├── exporter.py        ← export CSV / JSON
>│   └── utils.py           ← UUID, hash, pomocné funkce
>│
>├── tools/
>│   ├── scan.py            ← samostatně spustitelné
>│   ├── export.py
>│   ├── organize.py
>│   └── update_metadata.py
>│
>└── data/
>    └── library.json

# Soubor core/scanner.py

- rekurzivně projde složku
- vytvoří záznam
- vygeneruje UUID
- spočítá hash (doporučuji SHA256)
- uloží do DB

# Soubor core/database.py

- načtení library.json
- přidání knihy
- aktualizace knihy
- vyhledání podle UUID
- detekce duplicit podle hashe

core/metadata.py

Oddělená logika pro:

čtení PDF metadata

zápis PDF metadata

přejmenování souboru podle pravidla

Např:

{author} - {title} ({year}).pdf

core/organizer.py

Načte:

config/structure.json

Například:

{
  "odborna": {
    "informatika": {
      "programovani": {},
      "site": {},
      "ai": {}
    },
    "pedagogika": {}
  },
  "beletrie": {}
}

Funkce:

vytvoří chybějící složky

přesune soubor podle:

kategorie

tagu

nebo pravidla

core/exporter.py

Exporty:

JSON → CSV

JSON → čistý JSON

JSON → budoucí SQLite

tools/

Každý skript spustitelný:

scan.py
python tools/scan.py /knihy
export.py
python tools/export.py csv
organize.py
python tools/organize.py
update_metadata.py
python tools/update_metadata.py --id UUID

main.py – jednotné CLI

Použij argparse nebo ideálně typer (doporučuji).

Například:

python main.py scan /knihy
python main.py export csv
python main.py organize
python main.py update --id UUID

Main jen přeposílá do core modulů.

Budoucí rozšíření (už teď připravíme)

Proto rozdělíme vrstvy:

core  → čistá logika (bez CLI)
tools → CLI obaly
main  → unified CLI

Později přidáš:

ml/
    classifier.py
    duplicate_detector.py

api/
    fastapi_app.py

ui/
    web/
    desktop/

Co přidat
✔ EPUB podporu
✔ automatické přejmenování souboru podle metadata
✔ kontrolu integrity
✔ ML klasifikátor (automatická kategorie)
✔ REST API (FastAPI)
✔ Web UI

# Workflow

1. scan → CSV
2. upravíš metadata v CSV
3. import CSV → dict
4. rename
5. update metadata (PDF + XMP + ComicInfo)
6. případně reorganize folders
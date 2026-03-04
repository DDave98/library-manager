import json
import shutil
from pathlib import Path
from core.database import LibraryDatabase

# Načte strukturu složek z konfiguračního souboru
def load_structure(config_path="config/structure.json"):
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)

# Rekurzivně vytvoří složky podle zadané struktury
def create_structure(base_path, structure):
    for folder, subfolders in structure.items():
        path = Path(base_path) / folder
        path.mkdir(parents=True, exist_ok=True)
        create_structure(path, subfolders)

# Hlavní funkce pro organizaci knih podle kategorie
def organize_books(base_path):
    db = LibraryDatabase()
    structure = load_structure()

    create_structure(base_path, structure)

    for book in db.data:
        category = book.get("category")

        if category:
            target_folder = Path(base_path) / category
            target_folder.mkdir(parents=True, exist_ok=True)

            source = Path(book["filepath"])
            destination = target_folder / source.name

            if source.exists():
                shutil.move(str(source), str(destination))
                book["filepath"] = str(destination)

    db.save()
    print("Organizace dokončena.")
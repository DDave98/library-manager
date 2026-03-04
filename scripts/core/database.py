import json
from pathlib import Path

# Jednoduchá třída pro správu knihovny, která načítá a ukládá data do JSON souboru
class LibraryDatabase:

    # Inicializace databáze, načítá data z JSON souboru nebo vytváří nový, pokud neexistuje
    def __init__(self, db_path="data/library.json"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.data = self._load()

    # Načítá data z JSON souboru, pokud existuje, jinak vrací prázdný seznam
    def _load(self):
        if self.db_path.exists():
            with open(self.db_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    # Ukládá aktuální data do JSON souboru
    def save(self):
        with open(self.db_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)

    # Přidává novou knihu do databáze, pokud neexistuje duplicitní hash, a ukládá změny
    def add_book(self, book):
        if not self.find_by_hash(book["hash"]):
            self.data.append(book)
            self.save()
            return True
        return False
    
    # Hledá knihu podle hash hodnoty, vrací první shodu nebo None, pokud nenajde
    def find_by_hash(self, file_hash):
        return next((b for b in self.data if b["hash"] == file_hash), None)

    # Hledá knihu podle ID, vrací první shodu nebo None, pokud nenajde
    def find_by_id(self, book_id):
        return next((b for b in self.data if b["id"] == book_id), None)

    # Aktualizuje informace o knize podle ID, pokud kniha existuje, a ukládá změny
    def update_book(self, book_id, new_data):
        book = self.find_by_id(book_id)
        if book:
            book.update(new_data)
            self.save()
            return True
        return False
import os
from pathlib import Path
from core.utils import generate_uuid, compute_sha256, get_file_info
from core.metadata import read_pdf_metadata
from core.database import LibraryDatabase


SUPPORTED_EXTENSIONS = {".pdf"}


def scan_folder(folder_path):
    db = LibraryDatabase()

    for root, _, files in os.walk(folder_path):
        for file in files:
            ext = Path(file).suffix.lower()

            if ext in SUPPORTED_EXTENSIONS:
                full_path = os.path.join(root, file)
                print(f"Skenuji: {full_path}")

                file_hash = compute_sha256(full_path)

                if db.find_by_hash(file_hash):
                    print("  → Duplicitní soubor (přeskakuji)")
                    continue

                metadata = read_pdf_metadata(full_path)
                file_info = get_file_info(full_path)

                book_record = {
                    "id": generate_uuid(),
                    "hash": file_hash,
                    "metadata": metadata,
                    "tags": [],
                    "category": "",
                    "status": "new",
                    **file_info
                }

                db.add_book(book_record)

    print("Hotovo.")
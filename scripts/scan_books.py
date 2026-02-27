import os
import csv
import uuid
from pathlib import Path

from PyPDF2 import PdfReader
from ebooklib import epub

SUPPORTED_EXTENSIONS = {".pdf", ".epub"}


def extract_pdf_metadata(file_path):
    try:
        reader = PdfReader(file_path)
        metadata = reader.metadata or {}
        return {
            "title": metadata.get("/Title", ""),
            "author": metadata.get("/Author", ""),
            "producer": metadata.get("/Producer", ""),
            "creator": metadata.get("/Creator", ""),
        }
    except Exception as e:
        return {"error": f"PDF metadata error: {e}"}


def extract_epub_metadata(file_path):
    try:
        book = epub.read_epub(file_path)
        return {
            "title": ", ".join(book.get_metadata("DC", "title")[0]) if book.get_metadata("DC", "title") else "",
            "author": ", ".join([a[0] for a in book.get_metadata("DC", "creator")]) if book.get_metadata("DC", "creator") else "",
            "language": ", ".join([l[0] for l in book.get_metadata("DC", "language")]) if book.get_metadata("DC", "language") else "",
            "publisher": ", ".join([p[0] for p in book.get_metadata("DC", "publisher")]) if book.get_metadata("DC", "publisher") else "",
        }
    except Exception as e:
        return {"error": f"EPUB metadata error: {e}"}


def scan_books(root_folder, output_csv):
    rows = []

    for root, dirs, files in os.walk(root_folder):
        for file in files:
            ext = Path(file).suffix.lower()
            if ext in SUPPORTED_EXTENSIONS:
                full_path = os.path.join(root, file)

                print(f"Zpracovávám: {full_path}")

                book_uuid = str(uuid.uuid4())

                metadata = {}
                if ext == ".pdf":
                    metadata = extract_pdf_metadata(full_path)
                elif ext == ".epub":
                    metadata = extract_epub_metadata(full_path)

                row = {
                    "uuid": book_uuid,
                    "filename": file,
                    "filepath": full_path,
                    "extension": ext,
                    **metadata
                }

                rows.append(row)

    # sjednocení všech klíčů (protože metadata se liší)
    all_keys = set()
    for row in rows:
        all_keys.update(row.keys())

    all_keys = sorted(all_keys)

    with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=all_keys)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nHotovo. Uloženo do: {output_csv}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Rekurzivní scan knih a export do CSV")
    parser.add_argument("folder", help="Cesta ke kořenové složce s knihami")
    parser.add_argument("output", help="Výstupní CSV soubor")

    args = parser.parse_args()

    scan_books(args.folder, args.output)

# TODO
# hash souboru (SHA256 → detekce duplicit)
# velikost souboru
# datum vytvoření / úpravy
# vlastní interní ID (např. ID_KNIHA kompatibilní s tvým Excel systémem)
# export rovnou do SQLite místo CSV
# generování JSON pro import do Kavita

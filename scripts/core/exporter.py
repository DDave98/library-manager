import csv
from core.database import LibraryDatabase

# Funkce pro export dat z databáze do CSV formátu
def export_to_csv(output_file):
    db = LibraryDatabase()

    if not db.data:
        print("Databáze je prázdná.")
        return

    all_keys = set()
    for book in db.data:
        all_keys.update(book.keys())
        if "metadata" in book:
            all_keys.update(f"meta_{k}" for k in book["metadata"].keys())

    rows = []

    for book in db.data:
        row = book.copy()
        metadata = row.pop("metadata", {})

        for k, v in metadata.items():
            row[f"meta_{k}"] = v

        rows.append(row)

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=sorted(all_keys))
        writer.writeheader()
        writer.writerows(rows)

    print(f"Exportováno do {output_file}")
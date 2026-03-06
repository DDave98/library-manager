import argparse
import json
from pathlib import Path
from core.renamer import rename_file


def main():
    parser = argparse.ArgumentParser(description="Rename book file from metadata")

    parser.add_argument("file", help="Path to book file")
    parser.add_argument("metadata_json", help="Path to metadata JSON")
    parser.add_argument("--dry-run", action="store_true")

    args = parser.parse_args()

    file_path = Path(args.file)
    metadata = json.loads(Path(args.metadata_json).read_text(encoding="utf-8"))

    rename_file(file_path, metadata, dry_run=args.dry_run)

# python -m tools.rename_from_csv knihy.csv
if __name__ == "__main__":
    main()
    
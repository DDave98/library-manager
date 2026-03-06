import argparse
import json
from pathlib import Path
from core.comicinfo import save_comicinfo_file, embed_comicinfo_into_cbz


def main():
    parser = argparse.ArgumentParser(description="Generate ComicInfo.xml")

    parser.add_argument("file", help="Target file (pdf/epub/cbz)")
    parser.add_argument("metadata_json", help="Path to metadata json")

    args = parser.parse_args()

    file_path = Path(args.file)
    metadata = json.loads(Path(args.metadata_json).read_text(encoding="utf-8"))

    if file_path.suffix.lower() == ".cbz":
        embed_comicinfo_into_cbz(file_path, metadata)
        print("ComicInfo embedded into CBZ.")
    else:
        save_comicinfo_file(file_path, metadata)
        print("ComicInfo.xml saved next to file.")


if __name__ == "__main__":
    main()
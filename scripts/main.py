import argparse
from core.scanner import scan_folder
from core.exporter import export_to_csv
from core.organizer import organize_books


def main():
    parser = argparse.ArgumentParser(description="Knihovna CLI")
    subparsers = parser.add_subparsers(dest="command")

    scan_parser = subparsers.add_parser("scan")
    scan_parser.add_argument("folder")

    export_parser = subparsers.add_parser("export")
    export_parser.add_argument("output")

    organize_parser = subparsers.add_parser("organize")
    organize_parser.add_argument("base_path")

    args = parser.parse_args()

    if args.command == "scan":
        scan_folder(args.folder)

    elif args.command == "export":
        export_to_csv(args.output)

    elif args.command == "organize":
        organize_books(args.base_path)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
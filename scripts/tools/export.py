import sys
from core.exporter import export_to_csv

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Použití: python tools/export.py <output.csv>")
        sys.exit(1)

    export_to_csv(sys.argv[1])
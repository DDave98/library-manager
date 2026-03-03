import sys
from core.scanner import scan_folder

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Použití: python tools/scan.py <cesta_ke_složce>")
        sys.exit(1)

    scan_folder(sys.argv[1])
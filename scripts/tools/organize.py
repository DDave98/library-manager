import sys
from core.organizer import organize_books

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Použití: python tools/organize.py <cílová_složka>")
        sys.exit(1)

    organize_books(sys.argv[1])
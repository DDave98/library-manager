import re
from pathlib import Path


INVALID_CHARS = r'[<>:"/\\|?*]'


def sanitize_filename(name: str) -> str:
    """
    Remove invalid Windows filename characters.
    """
    name = re.sub(INVALID_CHARS, "", name)
    name = name.strip()
    return name


def build_filename(metadata: dict, extension: str) -> str:
    """
    Create filename in format: [Title] - [Author].ext
    """

    title = metadata.get("title") or "Unknown Title"

    author = metadata.get("writers") or metadata.get("author") or "Unknown Author"

    if isinstance(author, list):
        author = ", ".join(author)

    filename = f"{title} - {author}"
    filename = sanitize_filename(filename)

    return f"{filename}{extension}"


def resolve_collision(path: Path) -> Path:
    """
    If file exists, add (1), (2), etc.
    """
    if not path.exists():
        return path

    counter = 1
    stem = path.stem
    suffix = path.suffix
    parent = path.parent

    while True:
        new_path = parent / f"{stem} ({counter}){suffix}"
        if not new_path.exists():
            return new_path
        counter += 1


def rename_file(file_path: Path, metadata: dict, dry_run: bool = False) -> Path:
    """
    Rename file according to metadata.
    Returns new path.
    """

    new_name = build_filename(metadata, file_path.suffix)
    new_path = file_path.parent / new_name
    new_path = resolve_collision(new_path)

    if dry_run:
        print(f"[DRY RUN] {file_path.name} → {new_path.name}")
        return new_path

    file_path.rename(new_path)
    print(f"Renamed: {file_path.name} → {new_path.name}")

    return new_path
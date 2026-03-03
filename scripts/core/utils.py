import uuid
import hashlib
from pathlib import Path


def generate_uuid():
    return str(uuid.uuid4())


def compute_sha256(file_path, chunk_size=8192):
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(chunk_size):
            sha256.update(chunk)
    return sha256.hexdigest()


def get_file_info(file_path):
    path = Path(file_path)
    stat = path.stat()

    return {
        "filename": path.name,
        "filepath": str(path.resolve()),
        "size": stat.st_size,
        "created_at": stat.st_ctime,
        "modified_at": stat.st_mtime,
    }
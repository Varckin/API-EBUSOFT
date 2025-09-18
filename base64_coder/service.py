from pathlib import Path
import base64


def encode_string(data: str) -> str:
    """Encode a string into Base64."""
    encoded_bytes = base64.b64encode(data.encode("utf-8"))
    return encoded_bytes.decode("utf-8")

def decode_string(data: str) -> str:
    """Decode a Base64 string into plain text."""
    decoded_bytes = base64.b64decode(data.encode("utf-8"))
    return decoded_bytes.decode("utf-8")

def encode_file(content: bytes) -> str:
    """Encode file content into Base64."""
    encoded_bytes = base64.b64encode(content)
    return encoded_bytes.decode("utf-8")

def decode_file(data: str, filename: str, directory: Path) -> Path:
    """
    Decode Base64 string into a file.

    - Keeps the original filename
    - Adds suffixes (1), (2), ... if file already exists
    """
    decoded_bytes = base64.b64decode(data.encode("utf-8"))
    file_path = get_unique_filename(directory, filename)
    file_path.write_bytes(decoded_bytes)
    return file_path

def get_unique_filename(directory: Path, filename: str) -> Path:
    """
    Return a unique file path, preserving the original name.
    If a file exists, add suffix (1), (2), ...
    """
    base = Path(filename).stem
    ext = Path(filename).suffix
    candidate = directory / filename
    counter = 1

    while candidate.exists():
        candidate = directory / f"{base}({counter}){ext}"
        counter += 1

    return candidate

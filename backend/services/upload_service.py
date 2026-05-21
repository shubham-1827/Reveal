from pathlib import Path
from fastapi import UploadFile

UPLOAD_DIR = Path("uploads")
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB

ALLOWED_EXTENSIONS = [".exe"]


def validate_extension(filename: str) -> bool:
    return Path(filename).suffix.lower() in ALLOWED_EXTENSIONS


async def validate_file_size(file: UploadFile):
    contents = await file.read()

    if len(contents) > MAX_FILE_SIZE:
        return False

    await file.seek(0)
    return True


async def save_upload(file: UploadFile) -> str:

    if not file.filename:
        raise ValueError("Invalid filename")
    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    return str(file_path)

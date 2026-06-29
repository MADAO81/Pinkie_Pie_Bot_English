# bot/utils/file_utils.py
"""
File utilities for Pinkie Pie bot.

Author: MADAO81
Version: 2.0
"""

import os
from pathlib import Path
from typing import Optional, List
from datetime import datetime
from bot.config import Config


def ensure_directory(path: Path) -> bool:
    """Creates directory if it doesn't exist."""
    try:
        path.mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        print(f"Error creating directory {path}: {e}")
        return False


def save_file(data: bytes, filename: str, directory: Optional[Path] = None) -> Optional[Path]:
    """Saves file to directory."""
    if directory is None:
        directory = Config.DATA_DIR

    if not ensure_directory(directory):
        return None

    file_path = directory / filename

    try:
        with open(file_path, "wb") as f:
            f.write(data)
        return file_path
    except Exception as e:
        print(f"Error saving file {file_path}: {e}")
        return None


def load_file(file_path: Path) -> Optional[bytes]:
    """Loads file into memory."""
    try:
        with open(file_path, "rb") as f:
            return f.read()
    except Exception as e:
        print(f"Error loading file {file_path}: {e}")
        return None


def delete_file(file_path: Path) -> bool:
    """Deletes file."""
    try:
        if file_path.exists():
            os.remove(file_path)
            return True
        return False
    except Exception as e:
        print(f"Error deleting file {file_path}: {e}")
        return False


def delete_old_files(
    directory: Path,
    extension: Optional[str] = None,
    days_old: int = 7
) -> int:
    """Deletes old files from directory."""
    if not directory.exists():
        return 0

    deleted_count = 0
    now = datetime.now()

    for file_path in directory.iterdir():
        if file_path.is_file():
            if extension and not file_path.suffix == extension:
                continue

            modified_time = datetime.fromtimestamp(file_path.stat().st_mtime)
            age = (now - modified_time).days

            if age > days_old:
                if delete_file(file_path):
                    deleted_count += 1

    return deleted_count


def get_file_size(file_path: Path) -> int:
    """Returns file size in bytes."""
    try:
        return file_path.stat().st_size
    except Exception:
        return 0


def get_file_extension(filename: str) -> str:
    """Returns file extension."""
    return Path(filename).suffix


def list_files(
    directory: Path,
    extension: Optional[str] = None,
    sort_by_date: bool = False
) -> List[Path]:
    """Returns list of files in directory."""
    if not directory.exists():
        return []

    files = []
    for file_path in directory.iterdir():
        if file_path.is_file():
            if extension and not file_path.suffix == extension:
                continue
            files.append(file_path)

    if sort_by_date:
        files.sort(key=lambda x: x.stat().st_mtime)

    return files


def clean_temp_files():
    """Cleans temporary audio files older than 1 day."""
    audio_dir = Config.AUDIO_DIR
    if audio_dir.exists():
        deleted = delete_old_files(audio_dir, days_old=1)
        if deleted > 0:
            print(f"🧹 Deleted {deleted} temporary audio files")

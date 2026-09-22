import os
from pathlib import Path

import psutil

from psx.utils.display import header, sep


def cache_root() -> Path:
    return Path.home() / ".cache"


def cache_usage(root: Path | None = None) -> tuple[int, int]:
    root = root or cache_root()
    if not root.is_dir():
        return 0, 0

    total = 0
    files = 0
    for directory, _, filenames in os.walk(root, followlinks=False):
        for filename in filenames:
            path = Path(directory) / filename
            try:
                if not path.is_symlink():
                    total += path.stat().st_size
                    files += 1
            except OSError:
                continue
    return total, files


def format_size(size: int) -> str:
    units = ("B", "KB", "MB", "GB", "TB")
    value = float(size)
    for unit in units:
        if value < 1024 or unit == units[-1]:
            return f"{value:.1f} {unit}"
        value /= 1024
    return "0.0 B"


def clean_cache(root: Path | None = None) -> tuple[int, int]:
    root = root or cache_root()
    if not root.is_dir():
        return 0, 0

    removed_size = 0
    removed_files = 0
    for directory, dirnames, filenames in os.walk(root, topdown=False, followlinks=False):
        directory_path = Path(directory)
        for filename in filenames:
            path = directory_path / filename
            try:
                if path.is_symlink():
                    continue
                removed_size += path.stat().st_size
                path.unlink()
                removed_files += 1
            except OSError:
                continue

        for dirname in dirnames:
            path = directory_path / dirname
            try:
                if not path.is_symlink():
                    path.rmdir()
            except OSError:
                continue
    return removed_size, removed_files


def run(action: str | None = None) -> None:
    length = header("Clear Space")
    usage = psutil.disk_usage("/")
    cache_size, cache_files = cache_usage()

    print(f"{'Disk used:':12} {usage.percent:.0f}%")
    print(f"{'Free space:':12} {format_size(usage.free)}")
    print(f"{'User cache:':12} {format_size(cache_size)} ({cache_files} files)")

    if action in {"clean", "--clean"}:
        removed_size, removed_files = clean_cache()
        print(f"{'Cleaned:':12} {format_size(removed_size)} ({removed_files} files)")
    else:
        print(f"{'Action:':12} Run `psx clearspace clean` to clear user cache files.")

    sep(length)

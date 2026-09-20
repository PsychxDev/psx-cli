from importlib.metadata import version, PackageNotFoundError
from psx.utils.display import header, sep


def run():
    length = header("Version")

    try:
        pkg_version = version("psx-sys")
    except PackageNotFoundError:
        pkg_version = "unknown"

    print(f"{'Version:':12} PsX v{pkg_version}")
    sep(length)
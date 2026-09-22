from importlib.metadata import version
from psx.utils.display import header, sep

def run():
    length = header("Version")
    print("PsX v" + version("psx-sys"))
    sep(length)
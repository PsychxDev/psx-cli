from datetime import datetime
from psx.utils.display import header, sep

def run() :
    now = datetime.now()
    length = header("Datetime")
    print(f"{'Date:':5} {now.strftime('%Y-%m-%d')}")
    print(f"{'Time:':5} {now.strftime('%H-%M-%S')}")
    sep(length)
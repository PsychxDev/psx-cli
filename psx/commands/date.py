from datetime import datetime
from psx.utils.display import header, sep

def run() :
    now = datetime.now()
    length = header("Date & Time")
    print(f"{now.strftime('%-d-%-m-%Y')} |", end=' ')
    print(f"{now.strftime('%-I:%M %p')}")
    sep(length)
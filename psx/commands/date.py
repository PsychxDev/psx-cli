from datetime import datetime

from psx.utils.display import header, sep


def run() -> None:
    now = datetime.now()
    length = header("Date & Time")
    print(now.strftime("%-d-%-m-%Y | %-I:%M %p"))
    sep(length)
from datetime import datetime

from psx.utils.display import header, sep


def run() -> None:
    now = datetime.now()
    length = header("Datetime")
    print(now.strftime("%-d-%-m-%Y | %-I:%M %p"))
    sep(length)
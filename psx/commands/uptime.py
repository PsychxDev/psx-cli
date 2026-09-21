from psx.utils.display import header, sep

def run() :
    with open("/proc/uptime") as file:
        content = file.read()
        seconds = float(content.split()[0])
        days = int(seconds // 86400)
        remaining = seconds % 86400
        hours = int(remaining // 3600)
        remaining = remaining % 3600
        minutes = int(remaining // 60)

        length = header("Uptime")

        if days == 0 and hours == 0 :
            print(f"{'Uptime:':5} {minutes}m {seconds}s")

        elif days == 0 :
            print(f"{'Uptime:':5} {hours}h {minutes}m")

        elif hours == 0 :
            print(f"{'Uptime:':5} {days}d {minutes}m {seconds}s")

        else :
            print(f"{'Uptime:':5} {days}d {hours}h {minutes}m")

        sep(length)
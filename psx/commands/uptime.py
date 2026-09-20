from psx.utils.display import header, sep

def run() :
    with open("/proc/uptime") as file:
        content = file.read()
        total_seconds = int(float(content.split()[0]))
        days = int(total_seconds // 86400)
        remaining = total_seconds % 86400
        hours = int(remaining // 3600)
        remaining = remaining % 3600
        minutes = int(remaining // 60)
        seconds = int(remaining % 60)

        length = header("Uptime")

        if days == 0 and hours == 0 and minutes == 0:
            print(f"{'Uptime:':5} {seconds}s")

        elif days == 0 and hours == 0:
            print(f"{'Uptime:':5} {minutes}m {seconds}s")

        elif days == 0:
            print(f"{'Uptime:':5} {hours}h {minutes}m")

        elif hours == 0:
            print(f"{'Uptime:':5} {days}d {minutes}m")

        else :
            print(f"{'Uptime:':5} {days}d {hours}h {minutes}m")

        sep(length)
import platform
from psx.utils.display import header, sep

def cpu_info() :
    with open("/proc/cpuinfo") as file:
        for line in file:
            if "model name" in line:
                cpu = line.split(":")[1].strip()
                print(f"{'CPU:':13} {cpu}")
                break


def ram_info() :
    with open("/proc/meminfo") as file:
        for line in file:
            if "MemTotal" in line:
                ram_kb = int(line.split()[1].strip())
                ram_gb = ram_kb / 1000 / 1000
                print(f"{'Total RAM:':13} {ram_gb:.2f} GB")
                break


def run() :
    os_info = platform.freedesktop_os_release()
    length = header("System Info")
    print(f"{'OS:':13} {platform.system()} \n{'Distro:':13} {os_info["PRETTY_NAME"]} \n{'Kernel:':13} {platform.release()}")
    print(f"{'Architecture:':13} {platform.machine()}")
    cpu_info()
    ram_info()
    sep(length)

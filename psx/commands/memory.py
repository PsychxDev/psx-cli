from psx.utils.display import header, sep

def format_size(gb) :
    if gb < 1:
        return f"{gb * 1000:.0f} MB"
    else:
        return f"{gb:.2f} GB"

def run() :
    memory = {}

    with open("/proc/meminfo") as file:
        for line in file:
            key, value = line.split(":", 1)
            memory[key] = value.strip()

        total = int(memory["MemTotal"].split()[0])
        available = int(memory["MemAvailable"].split()[0])
        free = int(memory["MemFree"].split()[0])
        swap = int(memory["SwapTotal"].split()[0])
        cached = int(memory["Cached"].split()[0])
            
        total = total / 1000000
        available = available / 1000000
        free = free / 1000000
        swap = swap / 1000000
        used = total - available
        cached = cached / 1000000

        length = header("Memory Info")        
        print(f"{'Total:':11} {total:.2f} GB")
        print(f"{'Used:':11} {format_size(used)}")
        print(f"{'Available:':11} {format_size(available)}")
        print(f"{'Free:':11} {format_size(free)}")
        print(f"{'Cached:':11} {format_size(cached)}")
        print(f"{'Swap:':11} {format_size(swap)}")
        sep(length)
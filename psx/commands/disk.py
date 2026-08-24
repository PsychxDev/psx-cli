import subprocess
import json
from psx.utils.display import header, sep

def run() :
    result = subprocess.run(
        ["lsblk", "-J"],
        capture_output=True,
        text=True
    )
    data = json.loads(result.stdout)

    length = header("Disk Information")

    for devices in data['blockdevices'] :
        print(f"{'Name:':12} {devices['name']} \n{'Size:':12} {devices['size']}")
        print(f"{'Type:':12} {devices['type']}")
        print(f"{'Removeable:':12} Yes" if not 'false' else f"{'Removeable:':12} No")
        print(f"{'Mountpoints:':12} {devices['mountpoints']}" if not [None] else f"{'Mountpoints:':12} No Mount Points")

        if devices.get('children') :
            for partition in devices.get('children') :
                sep(length)
                print(f"{'Name:':12} {partition['name']}")
                print(f"{'Size:':12} {partition['size']}")
                print(f"{'Type:':12} {partition['type']}")
                print(f"{'Removeable:':12} Yes" if not 'false' else f"{'Removeable:':12} No")
                print(f"{'Mountpoints:':12} {devices['mountpoints']}" if not [None] else f"{'Mountpoints:':12} No Mount Points")
            sep(length)
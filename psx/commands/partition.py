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

    length = header("Partitions Info")
    for device in data["blockdevices"]:
        if device.get("children"):
            for partition in device["children"]:
                print(f"Name: {partition['name']:<4} | Size: {partition['size']:<7} | Type: {partition['type']}")
    sep(length)
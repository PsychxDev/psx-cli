import json
import subprocess

from psx.utils.display import header, sep


def display_device(device: dict, length: int, indent: str = "") -> None:
    name = device.get("name", "Unknown")
    size = device.get("size", "Unknown")
    device_type = device.get("type", "Unknown")
    removable = "Yes" if str(device.get("rm", "0")) == "1" else "No"

    mountpoints = [
        mountpoint
        for mountpoint in device.get("mountpoints", [])
        if mountpoint
    ]
    mounts = ", ".join(mountpoints) if mountpoints else "None"

    print(f"{indent}Name:        {name}")
    print(f"{indent}Size:        {size}")
    print(f"{indent}Type:        {device_type}")
    print(f"{indent}Removable:   {removable}")
    print(f"{indent}Mount Points: {mounts}")

    for partition in device.get("children", []):
        sep(length)
        display_device(partition, length, indent="  ")


def run() -> None:
    result = subprocess.run(
        ["lsblk", "-J", "-o", "NAME,SIZE,TYPE,RM,MOUNTPOINTS"],
        capture_output=True,
        text=True,
        check=True,
    )

    data = json.loads(result.stdout)
    length = header("Disk Information")

    for index, device in enumerate(data.get("blockdevices", [])):
        if index:
            sep(length)
        display_device(device, length)

    sep(length)
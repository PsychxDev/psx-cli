import json
import subprocess

from psx.utils.display import header, sep


def mount_display(mounts):
    cleaned = []
    for item in mounts or []:
        if isinstance(item, dict) and item.get("path"):
            cleaned.append(item["path"])
    return ", ".join(cleaned) if cleaned else "No Mount Points"


def run():
    result = subprocess.run(["lsblk", "-J"], capture_output=True, text=True)
    data = json.loads(result.stdout)

    length = header("Disk Information")

    for devices in data['blockdevices']:
        mount_text = mount_display(devices.get('mountpoints'))
        removable = bool(devices.get('rm', False))
        print(f"{'Name:':12} {devices['name']}")
        print(f"{'Size:':12} {devices['size']}")
        print(f"{'Type:':12} {devices['type']}")
        print(f"{'Removeable:':12} {'Yes' if removable else 'No'}")
        print(f"{'Mountpoints:':12} {mount_text}")

        if devices.get('children'):
            for partition in devices.get('children'):
                part_mounts = mount_display(partition.get('mountpoints'))
                part_removable = bool(partition.get('rm', False))
                print(f"{'Partition:':12} {partition['name']}")
                print(f"{'Size:':12} {partition['size']}")
                print(f"{'Type:':12} {partition['type']}")
                print(f"{'Removeable:':12} {'Yes' if part_removable else 'No'}")
                print(f"{'Mountpoints:':12} {part_mounts}")
                sep(length)

    sep(length)
import sys
from psx.commands import version
from psx.commands import help as help_command
from psx.commands import sysinfo
from psx.commands import memory
from psx.commands import partition
from psx.commands import disk
from psx.commands import date
from psx.commands import about
from psx.commands import uptime
from psx.commands import network
from psx.commands import domain
from psx.commands import ping
from psx.commands import dns
from psx.commands import todo
from psx.commands import profile
from psx.commands import health
from psx.commands import clearspace
from psx.commands import track

commands = {
    "help": {
        "run": help_command.run,
        "description": "Shows available commands.",
        "group": "Utility"
    },

    "version": {
        "run": version.run,
        "description": "Displays the current version of psx.",
        "group": "Utility"
    },

    "about": {
        "run": about.run,
        "description": "Information about the tool itself",
        "group": "Utility"
    },

    "sysinfo": {
        "run": sysinfo.run,
        "description": "Shows system information.",
        "group": "System"
    },

    "date": {
        "run": date.run,
        "description": "Shows the current date.",
        "group": "System"
    },

    "memory": {
        "run": memory.run,
        "description": "Shows information about random access memory.",
        "group": "System"
    },

    "disk": {
        "run": disk.run,
        "description": "Shows all disks detected on your device.",
        "group": "System"
    },

    "partition": {
        "run": partition.run,
        "description": "Shows all partitions on your PC.",
        "group": "System"
    },

    "uptime": {
        "run": uptime.run,
        "description": "Shows device Uptime.",
        "group": "System"
    },

    "network": {
        "run": network.run,
        "description": "Shows network information",
        "group": "Network"
    },

    "domain": {
        "run": domain.run,
        "description": "Looks up a domain, resolves DNS, and checks common web ports.",
        "group": "Network"
    },

    "ping": {
        "run": ping.run,
        "description": "Checks if a host responds to ICMP ping.",
        "group": "Network"
    },

    "dns": {
        "run": dns.run,
        "description": "Looks up DNS A and AAAA records for a domain.",
        "group": "Network"
    },

    "todo": {
        "run": todo.run,
        "description": "Manage a simple local todo list.",
        "group": "Utility"
    },

    "profile": {
        "run": profile.run,
        "description": "Shows a detailed system profile snapshot.",
        "group": "System"
    },

    "quick": {
        "run": profile.quick,
        "description": "Shows a compact system overview snapshot.",
        "group": "System"
    },

    "health": {
        "run": health.run,
        "description": "Shows a compact health summary of the machine.",
        "group": "System"
    },
    
    "clearspace": {
        "run": clearspace.run,
        "description": "Checks free space and clears user cache files.",
        "group": "System"
    },

    "track": {
        "run": track.run,
        "description": "Live monitor for system health and network activity.",
        "group": "System"
    },
}

def main() :
    args = sys.argv[1:]
    command = args[0] if args else None

    if command == "help" :
        commands["help"]["run"](commands)

    elif command in commands :
        if len(args) > 1 :
            commands[command]["run"](*args[1:])
        else :
            commands[command]["run"]()

    else :
        print(f"Unknown Command: {command}")

if __name__ == "__main__" :
    main()
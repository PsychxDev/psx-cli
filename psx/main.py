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

commands = {
    "help": {
        "run": help_command.run,
        "description": "Shows available commands."
    },

    "version": {
        "run": version.run,
        "description": "Displays the current version of psx."
    },

    "about": {
        "run": about.run,
        "description": "Information about the tool itself"
    },

    "sysinfo": {
        "run": sysinfo.run,
        "description": "Shows system information."
    },

    "date": {
        "run": date.run,
        "description": "Shows the current date."
    },

    "memory": {
        "run": memory.run,
        "description": "Shows information about random access memory."
    },

    "disk": {
        "run": disk.run,
        "description": "Shows all disks detected on your device."
    },

    "partition": {
        "run": partition.run,
        "description": "Shows all partitions on your PC."
    },

    "uptime": {
        "run": uptime.run,
        "description": "Shows device Uptime."
    },

    "network": {
        "run": network.run,
        "description": "Shows network information"
    },
}

def main() :
    args = sys.argv[1:]
    command = args[0]

    if command == "help" :
        commands["help"]["run"](commands)

    elif command in commands :
        commands[command]["run"]()

    else :
        print(f"Unknown Command: {command}")

if __name__ == "__main__" :
    main()
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
from psx.commands import weather

commands = {
    "help": {
        "run": help_command.run,
        "description": "Shows all available commands."
    },

    "version": {
        "run": version.run,
        "description": "Displays the current PsX version."
    },

    "about": {
        "run": about.run,
        "description": "Provides information about the tool itself."
    },

    "sysinfo": {
        "run": sysinfo.run,
        "description": "Shows system information."
    },

    "date": {
        "run": date.run,
        "description": "Shows the current date and time."
    },

    "memory": {
        "run": memory.run,
        "description": "Shows information about system memory."
    },

    "disk": {
        "run": disk.run,
        "description": "Shows all detected disks on your device."
    },

    "partition": {
        "run": partition.run,
        "description": "Shows all partitions on your system."
    },

    "uptime": {
        "run": uptime.run,
        "description": "Shows the system uptime."
    },

    "network": {
        "run": network.run,
        "description": "Shows network information."
    },

    "weather": {
        "run": weather.run,
        "description": "Shows the current weather."
    },
}

def main() :
    try:

        args = sys.argv[1:]
        command = args[0]

        if command == "help" :
            commands["help"]["run"](commands)

        elif command in commands :
            commands[command]["run"]()

        else :
            print(f"Unknown Command: {command}")

    except IndexError:
        print("Missing command, must be -> psx <command>")

if __name__ == "__main__" :
    main()
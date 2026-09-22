# PsX CLI

PsX CLI is a lightweight Python command-line utility that brings system information, diagnostics, monitoring, networking tools, and everyday utilities into a single terminal interface.

PsX is designed to provide useful system information and practical tools through a simple and consistent CLI experience.

## Features

- System information and hardware inspection
- Memory and disk information
- Partition inspection
- System uptime monitoring
- Detailed and compact system profiles
- System health monitoring
- Cache and storage cleanup
- Live system and network monitoring
- Network information and connectivity checks
- Domain and DNS lookup tools
- Local TODO list management
- Built-in help, version, and project information

## Commands

PsX currently provides 20 commands organized into three categories.

### System

| Command | Description |
| --- | --- |
| `sysinfo` | Shows system information. |
| `date` | Shows the current date. |
| `memory` | Shows information about random access memory. |
| `disk` | Shows all disks detected on your device. |
| `partition` | Shows all partitions on your PC. |
| `uptime` | Shows device uptime. |
| `profile` | Shows a detailed system profile snapshot. |
| `quick` | Shows a compact system overview snapshot. |
| `health` | Shows a compact health summary of the machine. |
| `clearspace` | Checks free space and clears user cache files. |
| `track` | Live monitor for system health and network activity. |

### Network

| Command | Description |
| --- | --- |
| `network` | Shows network information. |
| `domain` | Looks up a domain, resolves DNS, and checks common web ports. |
| `ping` | Checks if a host responds to ICMP ping. |
| `dns` | Looks up DNS A and AAAA records for a domain. |

### Utility

| Command | Description |
| --- | --- |
| `help` | Shows available commands. |
| `version` | Displays the current version of PsX. |
| `about` | Shows information about the tool itself. |
| `todo` | Manages a simple local TODO list. |

## Installation

Install PsX from PyPI:

```bash
pipx install psx-sys
````

After installation, run:

```bash
psx
```

## Usage

Launch PsX:

```bash
psx
```

Display the available commands:

```bash
psx help
```

Check the installed version:

```bash
psx version
```

Get information about PsX:

```bash
psx about
```

Commands that require additional input can be used according to their respective command syntax.

## Command Categories

### System Information

PsX provides multiple levels of system information, from individual hardware components to complete system snapshots.

`sysinfo`, `memory`, `disk`, `partition`, `profile`, and `quick` provide different views of the system, while `health` and `track` focus on the current state and activity of the machine.

### Network Tools

PsX includes several networking utilities for inspecting network configuration, checking connectivity, and gathering domain information.

The `domain` command can resolve a domain, retrieve its IP information, and check common web ports.

The `dns` command focuses specifically on DNS A and AAAA records.

### System Maintenance

The `clearspace` command checks available disk space and can clear user cache files with user confirmation.

### Productivity

PsX also includes a simple local TODO list through the `todo` command, allowing basic task management directly from the terminal.

## Design Goals

PsX is built around a few core principles:

* Keep useful tools accessible from one CLI.
* Provide clear and readable terminal output.
* Keep commands lightweight and practical.
* Make system information easy to access.
* Maintain consistent behavior across commands.
* Improve performance and usability over time.

## Performance and Improvements

PsX continuously receives improvements to command performance, output formatting, and overall usability.

Existing commands are regularly refined to provide cleaner output, reduce unnecessary operations, and make the CLI more responsive and consistent.

## Requirements

* Python 3.12 or newer
* A supported operating system
* Some commands may require access to system or network information available on the host system

## Project Status

PsX is actively developed.

The project is continuously expanding with new commands, improvements to existing utilities, performance optimizations, and better terminal output.

The long-term goal of PsX is to provide a practical and lightweight command-line toolkit for system management, diagnostics, networking, monitoring, and everyday terminal tasks.

## Author

Developed by PsychxDev.

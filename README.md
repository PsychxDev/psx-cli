# PSX CLI

PSX CLI is a lightweight Linux system utility written in Python. It gives you quick access to system information, resource usage, and live weather data directly from the terminal.

## Overview

This project is designed to make common system checks fast and simple. It focuses on a clean terminal interface and easy-to-read output.

## Features

* System information overview
* Memory usage details
* Disk and partition information
* Network status and IP information
* System uptime tracking
* Current date and time
* Live weather lookup
* Clean, readable terminal output
* Modular command-based structure

## Commands

* `help` — Show all available commands
* `about` — Show information about the project
* `version` — Show the current PSX version
* `sysinfo` — Show OS, distro, kernel, CPU, and RAM info
* `date` — Show the current date and time
* `network` — Show network status and interfaces
* `memory` — Show memory usage details
* `disk` — Show detected disks
* `partition` — Show system partitions
* `uptime` — Show system uptime
* `weather` — Show the current weather for your location

## Installation

Install the package with pip:

```bash
pip install psx-sys
```

Or install it in editable mode for development:

```bash
git clone https://github.com/your-username/psx-cli.git
cd psx-cli
pip install -e .
```

After installation, run:

```bash
psx help
```

## Usage

```bash
psx help
psx sysinfo
psx memory
psx disk
psx network
psx weather
psx date
psx uptime
```

## Example Output

```text
===== PsX Date & Time =====
20-9-2026 | 7:11 PM
===========================
```

## Project Structure

```text
psx-cli/
├── psx/
│   ├── commands/
│   ├── utils/
│   ├── __init__.py
│   └── main.py
├── README.md
├── pyproject.toml
├── LICENSE
└── .gitignore
```

## Release Notes

### v1.1.0

* Added a dynamic version command
* Improved output formatting and consistency
* Added weather support
* Improved offline network detection
* Improved English wording and command descriptions
* Overall cleanup and usability improvements

## License

This project is licensed under the MIT License.


# PSX CLI

A lightweight terminal-based system information utility written in Python.

## Description

PSX CLI is a simple Linux command-line tool that provides useful system information directly from the terminal.

The tool is designed to make common system information easy to access through simple commands.

## Features

* System information
* Memory usage
* Disk usage
* Partition information
* Network information
* System uptime
* Date and time information
* Clean terminal output
* Modular command structure

## Commands

* `about` — Show information about PSX
* `date` — Show the current date and time
* `disk` — Show disk usage
* `help` — Show available commands
* `sysinfo` — Show system information
* `memory` — Show memory usage
* `network` — Show network information
* `partition` — Show partition information
* `uptime` — Show system uptime
* `version` — Show the current PSX version

## Technologies Used

* Python
* psutil
* Linux
* Custom Python modules

## Installation

Install PSX using pipx:

```bash
pipx install psx
```

After installation, you can run PSX directly from the terminal:

```bash
psx
```

## Usage

Run PSX and choose a command:

```bash
psx
```

You can also use the available commands directly:

```bash
psx uptime
psx memory
psx disk
psx network
```

## Project Structure

```text
psx-cli/
├── psx/
│   ├── commands/
│   ├── utils/
│   ├── __init__.py
│   └── main.py
├── .gitignore
├── pyproject.toml
└── README.md
```

## Future Improvements

* More system information commands
* Better command output
* Additional network information
* Improved error handling
* More customization options

## License

This project is licensed under the MIT License.


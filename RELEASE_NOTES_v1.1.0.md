# PSX CLI v1.1.0

## Highlights

This release brings a cleaner output layout, improved system command accuracy, and a new weather feature.

## What's new

- Added a dynamic version command that reads the current package version automatically
- Improved command output consistency across the CLI
- Added `weather` command for live weather checks
- Improved offline network detection
- Fixed uptime and memory display issues
- Improved English wording and CLI descriptions

## Updated commands

- `help`
- `about`
- `version`
- `sysinfo`
- `date`
- `memory`
- `disk`
- `partition`
- `uptime`
- `network`
- `weather`

## Installation

```bash
pip install psx-sys==1.1.0
```

Or install from source:

```bash
git clone https://github.com/your-username/psx-cli.git
cd psx-cli
pip install -e .
```

## Example usage

```bash
psx help
psx sysinfo
psx network
psx weather
psx date
```

## Notes

This release is intended to be a stable, user-friendly update for Linux system information and monitoring tasks.

## GitHub release

Use the tag:

```bash
git tag -a v1.1.0 -m "Release v1.1.0"
git push origin main --tags
```

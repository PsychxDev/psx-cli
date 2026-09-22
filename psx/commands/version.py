from pathlib import Path
import tomllib


def run() -> None:
    pyproject = Path(__file__).parents[2] / "pyproject.toml"

    with pyproject.open("rb") as file:
        config = tomllib.load(file)

    app_version = config["project"]["version"]
    print(f"PsX v{app_version}")
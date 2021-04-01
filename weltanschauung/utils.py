from pathlib import Path
from jinja2 import Template, Environment, FileSystemLoader

__all__ = [
    "read_resource",
    "read_template",
]

_RESOURCE_DIR = Path(__file__).resolve().parent / "resource"


def read_resource(p: Path) -> str:
    with open(str(_RESOURCE_DIR / p), "r") as f:
        return f.read()


def read_template(p: Path) -> Template:
    return Environment(loader=FileSystemLoader(str(_RESOURCE_DIR))).from_string(
        read_resource(p)
    )

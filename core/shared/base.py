from pathlib import Path

def get_project_root() -> str:
    return str(Path(__file__).resolve().parent.parent)


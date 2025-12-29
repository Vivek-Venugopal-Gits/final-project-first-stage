from pathlib import Path
from agent.workspace import WORKSPACE_ROOT
import difflib


class FileToolError(Exception):
    pass


def _resolve_path(relative_path: str) -> Path:
    path = (WORKSPACE_ROOT / relative_path).resolve()
    if not str(path).startswith(str(WORKSPACE_ROOT)):
        raise FileToolError("Access outside workspace denied")
    return path


def read_file(path: str) -> str:
    file_path = _resolve_path(path)
    if not file_path.exists():
        raise FileToolError(f"File not found: {path}")
    return file_path.read_text(encoding="utf-8")


def write_file(path: str, content: str):
    file_path = _resolve_path(path)
    if file_path.exists():
        raise FileToolError(f"File already exists: {path}")
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content, encoding="utf-8")


def append_file(path: str, content: str):
    file_path = _resolve_path(path)
    if not file_path.exists():
        raise FileToolError(f"File not found: {path}")
    with file_path.open("a", encoding="utf-8") as f:
        f.write("\n\n" + content)


def update_file(path: str, new_content: str) -> str:
    file_path = _resolve_path(path)
    if not file_path.exists():
        raise FileToolError(f"File not found: {path}")
    old_content = file_path.read_text(encoding="utf-8")
    diff = "\n".join(
        difflib.unified_diff(
            old_content.splitlines(),
            new_content.splitlines(),
            fromfile="before",
            tofile="after",
            lineterm=""
        )
    )
    file_path.write_text(new_content, encoding="utf-8")
    return diff


def delete_file(path: str):
    file_path = _resolve_path(path)
    if not file_path.exists():
        raise FileToolError(f"File not found: {path}")
    file_path.unlink()

import json
from pathlib import Path
from datetime import datetime

from notebook.models import Note
from notebook.notebook import Notebook

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DEFAULT_FILE = DATA_DIR / "notebook.json"


def _note_to_dict(note: Note) -> dict:
    return {
        "id": note.id,
        "title": note.title,
        "content": note.content,
        "created_at": note.created_at.isoformat() if note.created_at else None,
        "tags": getattr(note, "tags", []),
    }


def _dict_to_note(data: dict) -> Note:
    created_at = None
    if data.get("created_at"):
        created_at = datetime.fromisoformat(data["created_at"])
    return Note(
        id=data["id"],
        title=data["title"],
        content=data["content"],
        created_at=created_at,
        tags=data.get("tags", []),
    )


def save_data(notebook: Notebook, filename: Path = DEFAULT_FILE) -> None:
    """Зберігає нотатки у JSON файл."""
    filename = Path(filename)
    filename.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "next_id": notebook._next_id,
        "notes": [_note_to_dict(n) for n in notebook._notes.values()],
    }
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def load_data(filename: Path = DEFAULT_FILE) -> Notebook:
    """Завантажує нотатки з JSON файлу."""
    filename = Path(filename)
    try:
        with open(filename, "r", encoding="utf-8") as f:
            payload = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return Notebook()

    notebook = Notebook()
    notebook._next_id = payload.get("next_id", 1)
    for data in payload.get("notes", []):
        note = _dict_to_note(data)
        notebook._notes[note.id] = note
    return notebook

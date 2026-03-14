import json
import pickle
from pathlib import Path

from notebook.models import Note
from notebook.notebook import Notebook


def _note_to_dict(note: Note) -> dict:
    return {
        "id": note.id,
        "title": note.title,
        "content": note.content,
        "created_at": note.created_at.isoformat() if note.created_at else None,
        "tags": getattr(note, "tags", None) or [],
    }


def _dict_to_note(data: dict) -> Note:
    from datetime import datetime
    created = data.get("created_at")
    if isinstance(created, str):
        created = datetime.fromisoformat(created)
    return Note(
        id=data["id"],
        title=data["title"],
        content=data["content"],
        created_at=created,
        tags=list(data.get("tags") or []),
    )


def save_data(notebook: Notebook, filename: str | Path = "notebook.json") -> None:
    data = {
        "next_id": notebook._next_id,
        "notes": [_note_to_dict(n) for n in notebook._notes.values()],
    }
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_data(filename: str | Path = "notebook.json") -> Notebook:
    path = Path(filename)
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        nb = Notebook()
        nb._next_id = data.get("next_id", 1)
        for item in data.get("notes", []):
            note = _dict_to_note(item)
            nb._notes[note.id] = note
        return nb
    except FileNotFoundError:
        pass
    except (json.JSONDecodeError, KeyError, TypeError, ValueError):
        pass
    pkl_name = str(path).replace(".json", ".pkl") if str(path).endswith(".json") else path
    if pkl_name == path and ".pkl" not in str(path):
        pkl_name = "notebook.pkl"
    try:
        with open(pkl_name, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return Notebook()

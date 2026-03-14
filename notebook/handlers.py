from notebook.notebook import Notebook
from notebook.search import search_notes_by_tag, sort_notes_by_tag, sort_notes_by_date
from core.utils import input_error
from core.theme import success, error, info, header


@input_error
def note_add(args: list[str], notebook: Notebook) -> str:
    if len(args) < 2:
        raise IndexError
    title, *rest = args
    content = " ".join(rest).strip() if rest else ""
    note = notebook.add(title, content)
    return success(f"Нотатку додано (id={note.id}).")


@input_error
def note_search(args: list[str], notebook: Notebook) -> str:
    query = " ".join(args).strip() if args else ""
    if query.startswith("#"):
        return note_search_tag(args, notebook)
    notes = notebook.search(query)
    if not notes:
        return info("Нотаток не знайдено.")
    return "\n".join(str(n) for n in notes)


@input_error
def note_delete(args: list[str], notebook: Notebook) -> str:
    if not args:
        raise IndexError
    raw_id = args[0]
    try:
        note_id = int(raw_id)
    except ValueError:
        raise ValueError("ID має бути числом.")
    if notebook.delete(note_id):
        return success(f"Нотатку {note_id} видалено.")
    raise ValueError("Нотатку не знайдено.")


@input_error
def note_edit(args: list[str], notebook: Notebook) -> str:
    if len(args) < 2:
        raise IndexError
    raw_id, *rest = args
    try:
        note_id = int(raw_id)
    except ValueError:
        raise ValueError("ID має бути числом.")
    note = notebook.get(note_id)
    if note is None:
        raise ValueError("Нотатку не знайдено.")
    new_content = " ".join(rest).strip() if rest else ""
    if new_content:
        notebook.edit(note_id, content=new_content)
    return success(f"Нотатку {note_id} оновлено.")


@input_error
def note_search_tag(args: list[str], notebook: Notebook) -> str:
    if not args:
        raise IndexError
    tag = args[0].lstrip("#")
    notes = search_notes_by_tag(notebook, tag)
    if not notes:
        return info(f"Нотаток з тегом #{tag} не знайдено.")
    return "\n".join(str(n) for n in notes)


@input_error
def note_sort_by_tag(args: list[str], notebook: Notebook) -> str:
    notes = sort_notes_by_tag(notebook)
    if not notes:
        return info("Нотаток немає.")
    return "\n".join(str(n) for n in notes)


@input_error
def note_sort_by_date(args: list[str], notebook: Notebook) -> str:
    reverse = args and args[0].lower() in ("desc", "зворотній")
    notes = sort_notes_by_date(notebook, reverse=reverse)
    if not notes:
        return info("Нотаток немає.")
    return "\n".join(str(n) for n in notes)

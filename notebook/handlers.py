from core.decorators import input_error
from core.table_utils import notes_table
from notebook.notebook import Notebook


def _parse_note_args(args: list[str]):
    tags = []
    rest = []
    for w in args:
        if w.startswith("#"):
            tags.append(w[1:].strip())
        else:
            rest.append(w)
    return rest, tags


@input_error
def note_add(args: list[str], notebook: Notebook) -> str:
    if len(args) < 2:
        raise IndexError
    rest, tags = _parse_note_args(args)
    title = rest[0]
    content = " ".join(rest[1:]).strip() if len(rest) > 1 else ""
    note = notebook.add(title, content, tags=tags if tags else None)
    return f"Нотатку додано (id={note.id})."


@input_error
def note_search(args: list[str], notebook: Notebook) -> str:
    query = " ".join(args).strip() if args else ""
    notes = notebook.search(query)
    if not notes:
        return "Нотаток не знайдено."
    return notes_table(notes)


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
        return f"Нотатку {note_id} видалено."
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
    rest, tags = _parse_note_args(rest)
    kwargs = {}
    if rest:
        kwargs["content"] = " ".join(rest).strip()
    if tags:
        kwargs["tags"] = tags
    note = notebook.edit(note_id, **kwargs) if kwargs else notebook.get(note_id)
    if note is None:
        raise ValueError("Нотатку не знайдено.")
    return f"Нотатку {note_id} оновлено."


@input_error
def note_sort(args: list[str], notebook: Notebook) -> str:
    kind = (args[0].lower() if args else "date").strip()
    if kind not in ("date", "tag"):
        raise ValueError("Допустимі значення: date, tag.")
    notes = notebook.sort_notes(by=kind)
    if not notes:
        return "Нотаток немає."
    return notes_table(notes)


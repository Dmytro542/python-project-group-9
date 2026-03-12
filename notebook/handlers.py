from address_book import input_error
from notebook.notebook import Notebook


@input_error
def note_add(args: list[str], notebook: Notebook) -> str:
    if len(args) < 2:
        raise IndexError
    title, *rest = args
    content = " ".join(rest).strip() if rest else ""
    note = notebook.add(title, content)
    return f"Нотатку додано (id={note.id})."


@input_error
def note_search(args: list[str], notebook: Notebook) -> str:
    query = " ".join(args).strip() if args else ""
    notes = notebook.search(query)
    if not notes:
        return "Нотаток не знайдено."
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
        return f"Нотатку {note_id} видалено."
    raise ValueError("Нотатку не знайдено.")


@input_error
def note_edit(args: list[str], notebook: Notebook) -> str:
    if len(args) < 2:
        raise IndexError
    raw_id, *rest = args
    try:
        note_id = int(raw_id)


        dsfsdfsddfsddf
    except ValueError:
        raise ValueError("ID має бути числом.")
    note = notebook.get(note_id)
    if note is None:
        raise ValueError("Нотатку не знайдено.")
    new_content = " ".join(rest).strip() if rest else ""
    if new_content:
        notebook.edit(note_id, content=new_content)
    return f"Нотатку {note_id} оновлено."

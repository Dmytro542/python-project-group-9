from notebook.notebook import Notebook
from notebook.search import search_notes_by_tag, sort_notes_by_tag, sort_notes_by_date


def input_error(func):
    """Декоратор обробляє KeyError, ValueError, IndexError у handler-функціях."""
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Контакт не знайдено."
        except ValueError as e:
            return str(e) if str(e) else "Невірний формат даних."
        except IndexError:
            return "Вкажіть усі аргументи для команди."
    return inner


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
    except ValueError:
        raise ValueError("ID має бути числом.")
    note = notebook.get(note_id)
    if note is None:
        raise ValueError("Нотатку не знайдено.")
    new_content = " ".join(rest).strip() if rest else ""
    if new_content:
        notebook.edit(note_id, content=new_content)
    return f"Нотатку {note_id} оновлено."


@input_error
def note_search_tag(args: list[str], notebook: Notebook) -> str:
    """Пошук нотаток за тегом (#тег)."""
    if not args:
        raise IndexError
    tag = args[0].lstrip("#")
    notes = search_notes_by_tag(notebook, tag)
    if not notes:
        return f"Нотаток з тегом #{tag} не знайдено."
    return "\n".join(str(n) for n in notes)


@input_error
def note_sort_by_tag(args: list[str], notebook: Notebook) -> str:
    """Сортування нотаток за тегами (алфавітно)."""
    notes = sort_notes_by_tag(notebook)
    if not notes:
        return "Нотаток немає."
    return "\n".join(str(n) for n in notes)


@input_error
def note_sort_by_date(args: list[str], notebook: Notebook) -> str:
    """Сортування нотаток за датою створення."""
    reverse = args and args[0].lower() in ("desc", "зворотній")
    notes = sort_notes_by_date(notebook, reverse=reverse)
    if not notes:
        return "Нотаток немає."
    return "\n".join(str(n) for n in notes)

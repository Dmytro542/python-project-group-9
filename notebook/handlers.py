from notebook.notebook import Notebook
from notebook.models import Note
from notebook.search import search_notes_by_tag, sort_notes_by_tag, sort_notes_by_date
from core.utils import input_error
from core.theme import success, error, info, header, render_table


NOTE_COLUMNS = ["ID", "Заголовок", "Зміст", "Теги", "Створено"]


NOTE_MAX_WIDTHS = [4, 15, 40, 20, 16]


def _note_to_row(note: Note) -> list[str]:
    """Конвертує нотатку у рядок таблиці."""
    tags = ", ".join(getattr(note, "tags", []) or []) or "—"
    created = note.created_at.strftime("%d.%m.%Y %H:%M") if note.created_at else "—"
    return [str(note.id), note.title, note.content, tags, created]


def _render_notes(notes: list[Note], title: str = "") -> str:
    """Відображає список нотаток таблицею."""
    rows = [_note_to_row(n) for n in notes]
    return render_table(NOTE_COLUMNS, rows, title, max_widths=NOTE_MAX_WIDTHS)


@input_error
def note_all(args: list[str], notebook: Notebook) -> str:
    notes = list(notebook.search(""))
    if not notes:
        return info("Нотаток немає.")
    return _render_notes(notes, f"Всього нотаток: {len(notes)}")


@input_error
def note_add(args: list[str], notebook: Notebook) -> str:
    if len(args) < 2:
        raise ValueError("Вкажіть заголовок та текст. Формат: add <заголовок> <текст> [#тег1 #тег2]")
    title = args[0]
    tags = [a.lstrip("#").lower() for a in args[1:] if a.startswith("#")]
    text_parts = [a for a in args[1:] if not a.startswith("#")]
    content = " ".join(text_parts).strip()
    if not content:
        raise ValueError("Вкажіть текст нотатки.")
    note = notebook.add(title, content, tags=tags)
    return success(f"Нотатку додано (id={note.id}).")


@input_error
def note_search(args: list[str], notebook: Notebook) -> str:
    query = " ".join(args).strip() if args else ""
    if query.startswith("#"):
        return note_search_tag(args, notebook)
    notes = notebook.search(query)
    if not notes:
        return info("Нотаток не знайдено.")
    title = f"Знайдено: {len(notes)}" if query else f"Всього нотаток: {len(notes)}"
    return _render_notes(notes, title)


@input_error
def note_delete(args: list[str], notebook: Notebook) -> str:
    if not args:
        raise ValueError("Вкажіть ID нотатки. Формат: delete <id>")
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
        raise ValueError("Вкажіть ID та новий текст. Формат: edit <id> <новий текст>")
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
        raise ValueError("Вкажіть тег для пошуку. Формат: search-tag <#тег>")
    tag = args[0].lstrip("#")
    notes = search_notes_by_tag(notebook, tag)
    if not notes:
        return info(f"Нотаток з тегом #{tag} не знайдено.")
    return _render_notes(notes, f"Тег: #{tag}")


@input_error
def note_sort_by_tag(args: list[str], notebook: Notebook) -> str:
    notes = sort_notes_by_tag(notebook)
    if not notes:
        return info("Нотаток немає.")
    return _render_notes(notes, "Сортовано за тегами")


@input_error
def note_sort_by_date(args: list[str], notebook: Notebook) -> str:
    reverse = bool(args) and args[0].lower() in ("desc", "зворотній")
    notes = sort_notes_by_date(notebook, reverse=reverse)
    if not notes:
        return info("Нотаток немає.")
    order = "нові → старі" if reverse else "старі → нові"
    return _render_notes(notes, f"Сортовано за датою ({order})")


@input_error
def note_add_tag(args: list[str], notebook: Notebook) -> str:
    if len(args) < 2:
        raise ValueError("Вкажіть ID та тег. Формат: add-tag <id> <#тег>")
    raw_id = args[0]
    try:
        note_id = int(raw_id)
    except ValueError:
        raise ValueError("ID має бути числом.")
    tag = args[1].lstrip("#").lower()
    if not tag:
        raise ValueError("Вкажіть тег.")
    note = notebook.add_tag(note_id, tag)
    if note is None:
        raise ValueError("Нотатку не знайдено.")
    return success(f"Тег #{tag} додано до нотатки {note_id}.")


@input_error
def note_del_tag(args: list[str], notebook: Notebook) -> str:
    if len(args) < 2:
        raise ValueError("Вкажіть ID та тег. Формат: del-tag <id> <#тег>")
    raw_id = args[0]
    try:
        note_id = int(raw_id)
    except ValueError:
        raise ValueError("ID має бути числом.")
    tag = args[1].lstrip("#").lower()
    if not tag:
        raise ValueError("Вкажіть тег.")
    result = notebook.remove_tag(note_id, tag)
    if result is None:
        raise ValueError("Нотатку не знайдено або тег відсутній.")
    return success(f"Тег #{tag} видалено з нотатки {note_id}.")

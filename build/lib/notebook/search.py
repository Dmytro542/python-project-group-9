from notebook.models import Note
from notebook.notebook import Notebook


def search_notes(notebook: Notebook, query: str) -> list[Note]:
    """Пошук нотаток за текстом у заголовку або вмісті."""
    return notebook.search(query)


def search_notes_by_tag(notebook: Notebook, tag: str) -> list[Note]:
    """Пошук нотаток за тегом."""
    tag = tag.lower().strip()
    results = []
    for note in notebook._notes.values():
        tags = _extract_tags(note)
        if tag in tags:
            results.append(note)
    return results


def sort_notes_by_tag(notebook: Notebook) -> list[Note]:
    """Сортування нотаток за першим тегом (алфавітно). Нотатки без тегів — в кінці."""
    def sort_key(note: Note) -> str:
        tags = _extract_tags(note)
        return tags[0] if tags else "я" * 10

    return sorted(notebook._notes.values(), key=sort_key)


def sort_notes_by_date(notebook: Notebook, reverse: bool = False) -> list[Note]:
    """Сортування нотаток за датою створення."""
    return sorted(
        notebook._notes.values(),
        key=lambda n: n.created_at,
        reverse=reverse
    )


def _extract_tags(note: Note) -> list[str]:
    """Витягує теги з поля tags нотатки."""
    return [tag.lower() for tag in (note.tags or [])]

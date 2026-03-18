from notebook.models import Note


class Notebook:
    def __init__(self):
        self._notes: dict[int, Note] = {}
        self._next_id: int = 1

    def add(self, title: str, content: str, tags: list[str] | None = None) -> Note:
        note = Note(id=self._next_id, title=title.strip(), content=content.strip(),
                     tags=tags or [])
        self._notes[self._next_id] = note
        self._next_id += 1
        return note

    def add_tag(self, note_id: int, tag: str) -> Note | None:
        note = self._notes.get(note_id)
        if note is None:
            return None
        tag = tag.strip().lower()
        if tag not in note.tags:
            note.tags.append(tag)
        return note

    def remove_tag(self, note_id: int, tag: str) -> Note | None:
        note = self._notes.get(note_id)
        if note is None:
            return None
        tag = tag.strip().lower()
        if tag in note.tags:
            note.tags.remove(tag)
            return note
        return None

    def get(self, note_id: int) -> Note | None:
        return self._notes.get(note_id)

    def search(self, query: str) -> list[Note]:
        if not query.strip():
            return list(self._notes.values())
        return [n for n in self._notes.values() if n.matches(query)]

    def delete(self, note_id: int) -> bool:
        if note_id in self._notes:
            del self._notes[note_id]
            return True
        return False

    def edit(self, note_id: int, title: str | None = None, content: str | None = None) -> Note | None:
        note = self._notes.get(note_id)
        if note is None:
            return None
        if title is not None:
            note.title = title.strip()
        if content is not None:
            note.content = content.strip()
        return note

    def __len__(self) -> int:
        return len(self._notes)

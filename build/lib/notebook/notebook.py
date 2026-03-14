from notebook.models import Note


class Notebook:
    def __init__(self):
        self._notes: dict[int, Note] = {}
        self._next_id: int = 1

    def add(self, title: str, content: str, tags: list[str] | None = None) -> Note:
        note = Note(
            id=self._next_id,
            title=title.strip(),
            content=content.strip(),
            tags=list(tags) if tags else [],
        )
        self._notes[self._next_id] = note
        self._next_id += 1
        return note

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

    def edit(
        self,
        note_id: int,
        title: str | None = None,
        content: str | None = None,
        tags: list[str] | None = None,
    ) -> Note | None:
        note = self._notes.get(note_id)
        if note is None:
            return None
        if title is not None:
            note.title = title.strip()
        if content is not None:
            note.content = content.strip()
        if tags is not None:
            note.tags = list(tags)
        return note

    def sort_notes(self, by: str = "date") -> list[Note]:
        if by == "date":
            return sorted(self._notes.values(), key=lambda n: n.created_at or "")
        if by == "tag":
            return sorted(
                self._notes.values(),
                key=lambda n: (", ".join(sorted(n.tags)) if n.tags else "\uffff", n.created_at or ""),
            )
        return list(self._notes.values())

    def __len__(self) -> int:
        return len(self._notes)

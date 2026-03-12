from dataclasses import dataclass
from datetime import datetime


@dataclass
class Note:
    id: int
    title: str
    content: str
    created_at: datetime | None = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

    def __str__(self) -> str:
        return f"[{self.id}] {self.title}: {self.content}"

    def matches(self, query: str) -> bool:
        q = query.lower()
        return q in self.title.lower() or q in self.content.lower()

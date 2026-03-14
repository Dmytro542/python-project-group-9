from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Note:
    id: int
    title: str
    content: str
    created_at: datetime | None = None
    tags: list[str] = field(default_factory=list)

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

    def __str__(self) -> str:
        tags_str = " [" + ", ".join(self.tags) + "]" if self.tags else ""
        return f"[{self.id}] {self.title}: {self.content}{tags_str}"

    def matches(self, query: str) -> bool:
        q = query.lower()
        if q in self.title.lower() or q in self.content.lower():
            return True
        for tag in self.tags:
            if q in tag.lower():
                return True
        return False

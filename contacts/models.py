from collections import UserDict

from fields.name import Name
from fields.phone import Phone
from fields.birthday import Birthday
from fields.email import Email


class Record:
    """Запис контакту: ім'я, список телефонів, опційно день народження."""

    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.email = None
        self.birthday = None
        self.tags = []

    def add_phone(self, phone) -> None:
        """Додає номер телефону до запису."""
        self.phones.append(Phone(phone))

    def add_email(self, email):
        """Додає email до контакту."""
        self.email = Email(email)

    def edit_email(self, new_email):
        """Оновлює email контакту."""
        if self.email is None:
            raise ValueError("Email не вказано.")
        self.email = Email(new_email)

    def remove_email(self):
        """Видаляє email контакту."""
        if self.email is None:
            raise ValueError("Email не вказано.")
        self.email = None

    def remove_phone(self, phone) -> None:
        """Видаляє номер телефону з запису."""
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return
        raise ValueError(f"Телефон {phone} не знайдено.")

    def edit_phone(self, old_phone, new_phone) -> None:
        """Замінює старий номер на новий."""
        for i, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[i] = Phone(new_phone)
                return
        raise ValueError(f"Телефон {old_phone} не знайдено.")

    def find_phone(self, phone) -> Phone | None:
        """Повертає об'єкт Phone з заданим номером або None."""
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_tag(self, tag) -> None:
        """Додає тег до запису."""
        if tag not in self.tags:
            self.tags.append(tag)

    def edit_tag(self, old_tag, new_tag) -> None:
        """Редагує існуючий тег."""
        if old_tag in self.tags:
            index = self.tags.index(old_tag)
            self.tags[index] = new_tag

    def remove_tag(self, tag) -> None:
        """Видаляє тег з запису."""
        if tag in self.tags:
            self.tags.remove(tag)

    def add_birthday(self, value) -> None:
        """Додає або оновлює день народження контакту."""
        self.birthday = Birthday(value)

    def __str__(self) -> str:
        lines = []

        lines.append(f"👤 {self.name.value}")

        if self.phones:
            lines.append("  ☎️ Phones:")
            for phone in self.phones:
                lines.append(f"     • {phone.value}")
        else:
            lines.append("  ☎️фдд Phones: —")

        if self.email:
            lines.append(f"  📧 Email: {self.email.value}")
        else:
            lines.append("  📧 Email: —")

        if self.birthday:
            lines.append(f"  🎂 Birthday: {self.birthday}")
        else:
            lines.append("  🎂 Birthday: —")

        if self.tags: lines.append(f" 🏷️ Tags: {', '.join(self.tags)}")
        else: lines.append(" 🏷️ Tags: —")

        return "\n".join(lines)


class AddressBook(UserDict):
    """Книга контактів: зберігання записів та керування ними."""

    def add_record(self, record) -> None:
        """Додає запис до книги."""
        self.data[record.name.value] = record

    def find(self, name) -> Record | None:
        """Повертає запис за іменем або None."""
        return self.data.get(name)

    def delete(self, name) -> None:
        """Видаляє запис за іменем."""
        if name in self.data:
            del self.data[name]

    def search(self, query) -> list[Record]:
        """
        Пошук контакту за іменем, телефоном або email.
        Повертає список записів, що підходять під запит.
        """
        results = []
        for record in self.data.values():
            if query.lower() in record.name.value.lower():
                results.append(record)
                continue
            if hasattr(record, 'email') and record.email and query.lower() in record.email.value.lower():
                results.append(record)
                continue
            for phone in record.phones:
                if query in phone.value:
                    results.append(record)
                    break
        return results

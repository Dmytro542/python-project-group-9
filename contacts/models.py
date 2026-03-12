from collections import UserDict

from fields.name import Name
from fields.phone import Phone
from fields.birthday import Birthday
from fields.email import Email


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.email = None
        self.birthday = None

    def add_phone(self, phone) -> None:
        self.phones.append(Phone(phone))

    def add_email(self, email):
        self.email = Email(email)

    def edit_email(self, new_email):
        if self.email is None:
            raise ValueError("Email не вказано.")
        self.email = Email(new_email)

    def remove_email(self):
        if self.email is None:
            raise ValueError("Email не вказано.")
        self.email = None

    def remove_phone(self, phone) -> None:
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return
        raise ValueError(f"Телефон {phone} не знайдено.")

    def edit_phone(self, old_phone, new_phone) -> None:
        for i, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[i] = Phone(new_phone)
                return
        raise ValueError(f"Телефон {old_phone} не знайдено.")

    def find_phone(self, phone) -> Phone | None:
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_birthday(self, value) -> None:
        self.birthday = Birthday(value)

    def __str__(self) -> str:
        phones_str = "; ".join(p.value for p in self.phones) if self.phones else "—"
        email_str = self.email.value if self.email else "—"
        birthday_str = str(self.birthday) if self.birthday else "—"
        return f"Contact name: {self.name.value}, phones: {phones_str}, email: {email_str}, birthday: {birthday_str}"


class AddressBook(UserDict):
    def add_record(self, record) -> None:
        self.data[record.name.value] = record

    def find(self, name) -> Record | None:
        return self.data.get(name)

    def delete(self, name) -> None:
        if name in self.data:
            del self.data[name]

    def search(self, query) -> list[Record]:
        results = []
        for record in self.data.values():
            if query.lower() in record.name.value.lower():
                results.append(record)
                continue
            if hasattr(record, "email") and record.email and query.lower() in record.email.value.lower():
                results.append(record)
                continue
            for phone in record.phones:
                if query in phone.value:
                    results.append(record)
                    break
        return results

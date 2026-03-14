import json
from pathlib import Path

from contacts.models import Record, AddressBook

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DEFAULT_FILE = DATA_DIR / "contacts.json"


def _record_to_dict(record: Record) -> dict:
    return {
        "name": record.name.value,
        "phones": [p.value for p in record.phones],
        "email": record.email.value if record.email else None,
        "birthday": str(record.birthday) if record.birthday else None,
        "tags": record.tags,
    }


def _dict_to_record(data: dict) -> Record:
    record = Record(data["name"])
    for phone in data.get("phones", []):
        record.add_phone(phone)
    if data.get("email"):
        record.add_email(data["email"])
    if data.get("birthday"):
        record.add_birthday(data["birthday"])
    for tag in data.get("tags", []):
        record.add_tag(tag)
    return record


def save_data(book: AddressBook, filename: Path = DEFAULT_FILE) -> None:
    """Зберігає адресну книгу у JSON файл."""
    filename = Path(filename)
    filename.parent.mkdir(parents=True, exist_ok=True)
    records = [_record_to_dict(r) for r in book.data.values()]
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)


def load_data(filename: Path = DEFAULT_FILE) -> AddressBook:
    """Завантажує адресну книгу з JSON файлу."""
    filename = Path(filename)
    try:
        with open(filename, "r", encoding="utf-8") as f:
            records = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return AddressBook()

    book = AddressBook()
    for data in records:
        record = _dict_to_record(data)
        book.add_record(record)
    return book

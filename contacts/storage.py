import json
import pickle

from contacts.models import AddressBook, Record


class _CompatUnpickler(pickle.Unpickler):
    _redirect = {"address_book": "contacts.models", "__main__": "contacts.models"}

    def find_class(self, module: str, name: str):
        if module in self._redirect and name in ("AddressBook", "Record"):
            module = self._redirect[module]
        return super().find_class(module, name)


def _record_to_dict(record: Record) -> dict:
    return {
        "name": record.name.value,
        "phones": [p.value for p in record.phones],
        "email": record.email.value if record.email else None,
        "birthday": str(record.birthday) if record.birthday else None,
        "address": record.address,
    }


def _dict_to_record(data: dict) -> Record:
    record = Record(data["name"])
    for p in data.get("phones") or []:
        record.add_phone(p)
    if data.get("email"):
        record.add_email(data["email"])
    if data.get("birthday"):
        record.add_birthday(data["birthday"])
    if data.get("address"):
        record.add_address(data["address"])
    return record


def save_data(book: AddressBook, filename: str = "addressbook.json") -> None:
    data = [_record_to_dict(r) for r in book.data.values()]
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_data(filename: str = "addressbook.json") -> AddressBook:
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        book = AddressBook()
        for item in data:
            record = _dict_to_record(item)
            book.add_record(record)
        return book
    except FileNotFoundError:
        pass
    except (json.JSONDecodeError, KeyError, TypeError, ValueError):
        pass
    pkl_name = filename.replace(".json", ".pkl") if filename.endswith(".json") else filename
    if pkl_name == filename and not filename.endswith(".pkl"):
        pkl_name = "addressbook.pkl"
    try:
        with open(pkl_name, "rb") as f:
            return _CompatUnpickler(f).load()
    except FileNotFoundError:
        return AddressBook()

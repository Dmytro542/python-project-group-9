import pickle

from contacts.models import AddressBook, Record


class _CompatUnpickler(pickle.Unpickler):
    _redirect = {"address_book": "contacts.models", "__main__": "contacts.models"}

    def find_class(self, module: str, name: str):
        if module in self._redirect and name in ("AddressBook", "Record"):
            module = self._redirect[module]
        return super().find_class(module, name)


def save_data(book: AddressBook, filename: str = "addressbook.pkl") -> None:
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename: str = "addressbook.pkl") -> AddressBook:
    try:
        with open(filename, "rb") as f:
            return _CompatUnpickler(f).load()
    except FileNotFoundError:
        return AddressBook()

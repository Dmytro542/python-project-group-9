from core.decorators import input_error
from core.table_utils import contacts_table
from contacts.models import AddressBook, Record
from birthdays import get_upcoming_birthdays
from core.help_text import show_help as _show_help


@input_error
def hello(args, book: AddressBook) -> str:
    return "Чим можу допомогти?"


@input_error
def help_cmd(args, book: AddressBook) -> str:
    return _show_help(args)


@input_error
def add_contact(args, book: AddressBook) -> str:
    name, phone, *_ = args
    record = book.find(name)
    message = "Контакт оновлено."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Контакт додано."
    if phone:
        record.add_phone(phone)
    return message


@input_error
def change_contact(args, book: AddressBook) -> str:
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError
    record.edit_phone(old_phone, new_phone)
    return "Номер оновлено."


@input_error
def show_phone(args, book: AddressBook) -> str:
    name, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError
    if not record.phones:
        return f"{name}: телефони не вказані."
    return f"{name}: {', '.join(p.value for p in record.phones)}"


@input_error
def show_all(args, book: AddressBook) -> str:
    if not book.data:
        return "Адресна книга порожня."
    return contacts_table(book.data.values())


@input_error
def add_birthday(args, book: AddressBook) -> str:
    name, birthday_str, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError
    record.add_birthday(birthday_str)
    return "День народження додано."


@input_error
def add_email(args, book: AddressBook) -> str:
    name, email, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError
    record.add_email(email)
    return "Email додано."


@input_error
def add_address(args, book: AddressBook) -> str:
    if len(args) < 2:
        raise IndexError
    name = args[0]
    address = " ".join(args[1:]).strip()
    record = book.find(name)
    if record is None:
        raise KeyError
    record.add_address(address)
    return "Адресу додано."


@input_error
def show_birthday(args, book: AddressBook) -> str:
    name, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError
    if record.birthday is None:
        return f"У контакту {name} не вказано день народження."
    return f"{name}: {record.birthday}"


@input_error
def show_contact(args, book: AddressBook) -> str:
    name, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError
    phones = ", ".join(p.value for p in record.phones) if record.phones else "—"
    email = record.email.value if record.email else "—"
    birthday = str(record.birthday) if record.birthday else "—"
    address = record.address if record.address else "—"
    return (
        f"Ім'я: {record.name.value}\n"
        f"Телефони: {phones}\n"
        f"Email: {email}\n"
        f"Адреса: {address}\n"
        f"День народження: {birthday}"
    )


@input_error
def birthdays(args, book: AddressBook) -> str:
    days = int(args[0]) if args else 7
    upcoming = get_upcoming_birthdays(book, days)
    if not upcoming:
        return f"На протязі {days} днів, дні народження ніхто не святкує."
    return "\n".join(
        f"Привітання з Днем Народження {item['name']}: {item['congratulation_date']}" for item in upcoming
    )


@input_error
def search_contact(args, book: AddressBook) -> str:
    query, *_ = args
    results = book.search(query)
    if not results:
        return "Контактів, що підходять під запит, не знайдено."
    return contacts_table(results)


@input_error
def delete_contact(args, book: AddressBook) -> str:
    if not args:
        raise IndexError
    name = args[0]
    if book.find(name) is None:
        raise KeyError
    book.delete(name)
    return f"Контакт «{name}» видалено."

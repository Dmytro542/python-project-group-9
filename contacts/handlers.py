from contacts.models import Record, AddressBook
from contacts.birthdays import get_upcoming_birthdays
from core.utils import input_error
from core.theme import success, error, info, header, render_table


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
    return success(message)


@input_error
def change_contact(args, book: AddressBook) -> str:
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError
    record.edit_phone(old_phone, new_phone)
    return success("Номер оновлено.")


@input_error
def show_phone(args, book: AddressBook) -> str:
    name, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError
    if not record.phones:
        return info(f"{name}: телефони не вказані.")
    return info(f"{name}: {', '.join(p.value for p in record.phones)}")


def _record_to_row(record: Record) -> list[str]:
    """Конвертує контакт у рядок таблиці."""
    phones = ", ".join(p.value for p in record.phones) if record.phones else "—"
    email = record.email.value if record.email else "—"
    birthday = str(record.birthday) if record.birthday else "—"
    tags = ", ".join(record.tags) if record.tags else "—"
    return [record.name.value, phones, email, birthday, tags]


CONTACT_COLUMNS = ["👤 Ім'я", "☎️ Телефони", "📧 Email", "🎂 День народж.", "🏷️ Теги"]


@input_error
def show_all(args, book: AddressBook) -> str:
    if not book.data:
        return info("Адресна книга порожня.")
    rows = [_record_to_row(r) for r in book.data.values()]
    return render_table(CONTACT_COLUMNS, rows, f"Всього контактів: {len(rows)}")


@input_error
def add_birthday(args, book: AddressBook) -> str:
    name, birthday_str, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError
    record.add_birthday(birthday_str)
    return success("День народження додано.")


@input_error
def add_email(args, book: AddressBook):
    name, email, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError
    record.add_email(email)
    return success("Email додано.")


@input_error
def show_birthday(args, book: AddressBook) -> str:
    name, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError
    if record.birthday is None:
        return info(f"У контакту {name} не вказано день народження.")
    return info(f"{name}: {record.birthday}")


@input_error
def show_contact(args, book: AddressBook) -> str:
    name, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError
    rows = [_record_to_row(record)]
    return render_table(CONTACT_COLUMNS, rows)


@input_error
def birthdays(args, book: AddressBook) -> str:
    days = int(args[0]) if args else 7
    upcoming = get_upcoming_birthdays(book, days)
    if not upcoming:
        return info(f"На протязі {days} днів, дні народження ніхто не святкує.")
    rows = [[item["name"], item["congratulation_date"]] for item in upcoming]
    return render_table(["Ім'я", "Дата привітання"], rows, f"Дні народження ({days} днів)")


@input_error
def search_contact(args, book: AddressBook) -> str:
    query, *_ = args
    results = book.search(query)
    if not results:
        return info("Контактів не знайдено.")
    rows = [_record_to_row(r) for r in results]
    return render_table(CONTACT_COLUMNS, rows, f"Знайдено: {len(results)}")


@input_error
def add_tag_to_contact(args, book: AddressBook):
    name, tag, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError
    record.add_tag(tag)
    return success(f"Тег '{tag}' додано для {name}.")


@input_error
def edit_tag_of_contact(args, book: AddressBook):
    name, old_tag, new_tag, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError
    record.edit_tag(old_tag, new_tag)
    return success(f"Тег '{old_tag}' замінено на '{new_tag}' для {name}.")


@input_error
def remove_tag_from_contact(args, book: AddressBook):
    name, tag, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError
    record.remove_tag(tag)
    return success(f"Тег '{tag}' видалено з {name}.")

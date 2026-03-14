from contacts.models import Record, AddressBook
from contacts.birthdays import get_upcoming_birthdays


def input_error(func):
    """Декоратор обробляє KeyError, ValueError, IndexError у handler-функціях."""

    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Контакт не знайдено."
        except ValueError as e:
            return str(e) if str(e) else "Невірний формат даних."
        except IndexError:
            return "Вкажіть усі аргументи для команди."

    return inner


def parse_input(user_input: str) -> tuple[str | None, list[str]]:
    """Розбиває введений рядок на команду та список аргументів."""
    parts = user_input.strip().split()
    if not parts:
        return None, []
    return parts[0].lower(), parts[1:]


@input_error
def add_contact(args, book: AddressBook) -> str:
    """Додає новий контакт або телефон до існуючого контакту."""
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
    """Змінює телефонний номер контакту: change [ім'я] [старий] [новий]."""
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError
    record.edit_phone(old_phone, new_phone)
    return "Номер оновлено."


@input_error
def show_phone(args, book: AddressBook) -> str:
    """Показує телефони контакту за іменем."""
    name, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError
    if not record.phones:
        return f"{name}: телефони не вказані."
    return f"{name}: {', '.join(p.value for p in record.phones)}"


@input_error
def show_all(args, book: AddressBook) -> str:
    """Показує всі контакти в адресній книзі."""
    if not book.data:
        return "Адресна книга порожня."

    return "\n\n".join(str(record) for record in book.data.values())


@input_error
def add_birthday(args, book: AddressBook) -> str:
    """Додає день народження контакту. Формат: DD.MM.YYYY."""
    name, birthday_str, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError
    record.add_birthday(birthday_str)
    return "День народження додано."


@input_error
def add_email(args, book: AddressBook):
    name, email, *_ = args
    record = book.find(name)

    if record is None:
        raise KeyError

    record.add_email(email)

    return "Email додано."


@input_error
def show_birthday(args, book: AddressBook) -> str:
    """Показує день народження контакту."""
    name, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError
    if record.birthday is None:
        return f"У контакту {name} не вказано день народження."
    return f"{name}: {record.birthday}"


@input_error
def show_contact(args, book: AddressBook) -> str:
    """Показує повну інформацію про контакт."""
    name, *_ = args
    record = book.find(name)

    if record is None:
        raise KeyError

    phones = ", ".join(p.value for p in record.phones) if record.phones else "—"
    email = record.email.value if record.email else "—"
    birthday = str(record.birthday) if record.birthday else "—"

    return (
        f"Ім'я: {record.name.value}\n"
        f"Телефони: {phones}\n"
        f"Email: {email}\n"
        f"День народження: {birthday}"
    )


@input_error
def birthdays(args, book: AddressBook) -> str:
    """Повертає список контактів з днями народження на протязі n днів."""
    days = int(args[0]) if args else 7

    upcoming = get_upcoming_birthdays(book, days)
    if not upcoming:
        return f"На протязі {days} днів, дні народження ніхто не святкує."
    return "\n".join(
        f"Привітання з Днем Народження {item['name']}: {item['congratulation_date']}" for item in upcoming
    )


@input_error
def search_contact(args, book: AddressBook) -> str:
    """Пошук контактів за ім'ям, телефоном або email."""
    query, *_ = args
    results = book.search(query)
    if not results:
        return "Контактів, що підходять під запит, не знайдено."
    lines = []
    for record in results:
        phones_str = ", ".join(p.value for p in record.phones) if record.phones else "—"
        email_str = record.email.value if hasattr(record, 'email') and record.email else "—"
        lines.append(f"{record.name.value}: телефони: {phones_str}, email: {email_str}")
    return "\n".join(lines)


@input_error
def add_tag_to_contact(args, book: AddressBook):
    name, tag, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError
    record.add_tag(tag)
    return f"Тег '{tag}' додано для контакту {name}."


@input_error
def edit_tag_of_contact(args, book: AddressBook):
    name, old_tag, new_tag, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError
    record.edit_tag(old_tag, new_tag)
    return f"Тег '{old_tag}' замінено на '{new_tag}' для контакту {name}."


@input_error
def remove_tag_from_contact(args, book: AddressBook):
    name, tag, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError
    record.remove_tag(tag)
    return f"Тег '{tag}' видалено з контакту {name}."

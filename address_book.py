# ── Імпорти ───────────────────────────────────────────────────────────────────

import calendar
import pickle
from collections import UserDict
from datetime import date, datetime, timedelta
from fields.name import Name
from fields.phone import Phone
from fields.birthday import Birthday
from fields.email import Email


# ── Утиліти ───────────────────────────────────────────────────────────────────

def _birthday_in_year(birth: date, year: int) -> date:
    if birth.month == 2 and birth.day == 29 and not calendar.isleap(year):
        return date(year, 2, 28)
    return birth.replace(year=year)


# ── Декоратор ─────────────────────────────────────────────────────────────────

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

# ── Record ────────────────────────────────────────────────────────────────────

class Record:
    """Запис контакту: ім'я, список телефонів, опційно день народження."""

    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.email = None
        self.birthday = None

    def add_phone(self, phone) -> None:
        """Додає номер телефону до запису."""
        self.phones.append(Phone(phone))

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

    def add_birthday(self, value) -> None:
        """Додає або оновлює день народження контакту."""
        self.birthday = Birthday(value)

    def add_email(self, email):
        self.email = Email(email)

    def __str__(self) -> str:
        phones_str = "; ".join(p.value for p in self.phones) if self.phones else "—"
        email_str = self.email.value if self.email else "—"

        return f"Contact name: {self.name.value}, phones: {phones_str}, email: {email_str}"

# ── AddressBook ───────────────────────────────────────────────────────────────

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

    def get_upcoming_birthdays(self) -> list[dict[str, str]]:
        """
        Повертає список контактів, яких потрібно привітати протягом наступних 7 днів.
        Вихідні (субота, неділя) переносяться на понеділок.
        """
        today = date.today()
        result = []
        for record in self.data.values():
            if record.birthday is None:
                continue
            birth = record.birthday.value
            birthday_this_year = _birthday_in_year(birth, today.year)
            delta_days = (birthday_this_year - today).days
            if delta_days < 0:
                birthday_this_year = _birthday_in_year(birth, today.year + 1)
                delta_days = (birthday_this_year - today).days
            if 0 <= delta_days <= 7:
                congratulation_date = birthday_this_year
                if congratulation_date.weekday() == 5:
                    congratulation_date += timedelta(days=2)
                elif congratulation_date.weekday() == 6:
                    congratulation_date += timedelta(days=1)
                result.append({
                    "name": record.name.value,
                    "congratulation_date": congratulation_date.strftime("%d.%m.%Y"),
                })
        return result


# ── Серіалізація ──────────────────────────────────────────────────────────────

def save_data(book: AddressBook, filename: str = "addressbook.pkl") -> None:
    """Зберігає адресну книгу у файл за допомогою pickle."""
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename: str = "addressbook.pkl") -> AddressBook:
    """Завантажує адресну книгу з файлу. Якщо файлу немає — повертає порожню книгу."""
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()


# ── Handlers ──────────────────────────────────────────────────────────────────

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
    lines = []
    for record in book.data.values():
        phones_str = ", ".join(p.value for p in record.phones) if record.phones else "—"
        lines.append(f"{record.name.value}: {phones_str}")
    return "\n".join(lines)


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
    """Повертає список контактів з днями народження на наступному тижні."""
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "На наступному тижні днів народження немає."
    return "\n".join(
        f"{item['name']}: {item['congratulation_date']}" for item in upcoming
    )


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    """Головний цикл бота з адресною книгою. Книга завантажується при старті, зберігається при виході."""
    book = load_data()
    commands = {
        "hello": lambda args, book: "Чим можу допомогти?",
        "add": add_contact,
        "change": change_contact,
        "phone": show_phone,
        "all": show_all,
        "add-birthday": add_birthday,
        "show-birthday": show_birthday,
        "birthdays": birthdays,
        "add-email": add_email,
        "show": show_contact,  # ← новая команда
    }
    print("Вітаю до бота-помічника!")
    while True:
        user_input = input("Введіть команду: ")
        command, args = parse_input(user_input)

        if command in ("close", "exit"):
            save_data(book)
            print("До зустрічі!")
            break
        if not command:
            continue
        if command in commands:
            print(commands[command](args, book))
        else:
            hint = ", ".join(commands.keys()) + ", close, exit"
            print(f"Невірна команда. Доступні: {hint}")


if __name__ == "__main__":
    main()

# ── Імпорти ───────────────────────────────────────────────────────────────────


import pickle
from collections import UserDict
from fields.name import Name
from fields.phone import Phone
from fields.birthday import Birthday
from fields.email import Email
from birthdays.get_upcoming_birthdays import get_upcoming_birthdays
from notebook.storage import load_data as load_notebook, save_data as save_notebook
from notebook.handlers import note_add, note_search, note_delete, note_edit, note_search_tag, note_sort_by_tag, note_sort_by_date


# ── Утиліти ───────────────────────────────────────────────────────────────────


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
        self.tags = []  # список тегів для цього контакту
        
    def add_phone(self, phone) -> None:
        """Додає номер телефону до запису."""
        self.phones.append(Phone(phone))

# NEW

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

    # UPD (NEW)
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

    # NEW
    def search(self, query) -> list[Record]:
        """
        Пошук контакту за іменем, телефоном або email.
        Повертає список записів, що підходять під запит.
        """
        results = []
        for record in self.data.values():
            # Пошук по імені
            if query.lower() in record.name.value.lower():
                results.append(record)
                continue
            # Пошук по email
            if hasattr(record, 'email') and record.email and query.lower() in record.email.value.lower():
                results.append(record)
                continue
            # Пошук по телефону
            for phone in record.phones:
                if query in phone.value:
                    results.append(record)
                    break
        return results

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


# ── Довідка (help) ────────────────────────────────────────────────────────────

HELP: dict[str, tuple[str, str]] = {
    "hello": ("hello", "Привітання."),
    "add": ("add <ім'я> <телефон>", "Додати контакт або телефон до існуючого (телефон — 10 цифр)."),
    "change": ("change <ім'я> <старий_телефон> <новий_телефон>", "Змінити номер телефону контакту."),
    "phone": ("phone <ім'я>", "Показати телефони контакту."),
    "all": ("all", "Показати всі контакти."),
    "add-birthday": ("add-birthday <ім'я> <DD.MM.YYYY>", "Додати день народження контакту."),
    "show-birthday": ("show-birthday <ім'я>", "Показати день народження контакту."),
    "birthdays": ("birthdays", "Дні народження на найближчий тиждень."),
    "note-add": ("note-add <заголовок> <текст нотатки>", "Додати нотатку (заголовок і текст через пробіл)."),
    "note-search": ("note-search [запит]", "Пошук нотаток за текстом; без запиту — показати всі."),
    "note-search-tag": ("note-search-tag <#тег>", "Пошук нотаток за тегом (наприклад: #робота)."),
    "note-sort-tag": ("note-sort-tag", "Показати всі нотатки відсортовані за тегами."),
    "note-sort-date": ("note-sort-date [desc]", "Показати нотатки відсортовані за датою (desc — від нових)."),
    "note-delete": ("note-delete <id>", "Видалити нотатку за номером id."),
    "note-edit": ("note-edit <id> <новий текст>", "Змінити вміст нотатки за id."),
    "help": ("help [команда]", "Довідка: усі команди або деталі по одній команді."),
}


def show_help(args: list[str]) -> str:
    if not args:
        contact_cmds = [c for c in HELP if not c.startswith("note-") and c != "help"]
        note_cmds = ["note-add", "note-search", "note-search-tag", "note-sort-tag", "note-sort-date", "note-delete", "note-edit"]
        lines = [
            "Контакти:",
            *(_format_help_row(c, HELP[c][0], HELP[c][1]) for c in contact_cmds),
            "",
            "Блокнот:",
            *(_format_help_row(c, HELP[c][0], HELP[c][1]) for c in note_cmds),
            "",
            "Інше:",
            "  help [команда]   — ця довідка",
            "  close / exit     — вихід з бота",
        ]
        return "\n".join(lines)
    cmd = args[0].lower()
    if cmd not in HELP:
        return f"Невідома команда «{cmd}». Введіть help без аргументів для списку команд."
    usage, desc = HELP[cmd]
    return f"  {usage}\n  -> {desc}"


def _format_help_row(cmd: str, usage: str, desc: str) -> str:
    return f"  {usage:<45} — {desc}"


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
def search_contact(args, book: AddressBook) -> str: # NEW
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
    
# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    """Головний цикл бота з адресною книгою та блокнотом."""
    book = load_data()
    notebook = load_notebook()
    commands = {
        "hello": lambda args, book: "Чим можу допомогти?",
        "help": lambda args, book: show_help(args),
        "add": add_contact,
        "change": change_contact,
        "phone": show_phone,
        "all": show_all,
        "add-birthday": add_birthday,
        "show-birthday": show_birthday,
        "show-birthdays": birthdays,
        "search": search_contact,  # <-- додано
        "add-email": add_email,
        "show": show_contact,  # ← новая команда
        "add-tag": add_tag_to_contact,
        "edit-tag": edit_tag_of_contact,
        "remove-tag": remove_tag_from_contact,
    }
    note_commands = {
        "note-add": note_add,
        "note-search": note_search,
        "note-search-tag": note_search_tag,
        "note-sort-tag": note_sort_by_tag,
        "note-sort-date": note_sort_by_date,
        "note-delete": note_delete,
        "note-edit": note_edit,
    }
    all_commands = {**commands, **note_commands}
    try:
        from prompt_helper import prompt_input
    except ImportError:
        prompt_input = None

    print("Вітаю до бота-помічника!")
    while True:
        try:
            if prompt_input:
                user_input = prompt_input()
            else:
                user_input = input("Введіть команду: ")
        except (KeyboardInterrupt, EOFError):
            save_data(book)
            save_notebook(notebook)
            print("\nДо зустрічі!")
            break
        command, args = parse_input(user_input)

        if command in ("close", "exit"):
            save_data(book)
            save_notebook(notebook)
            print("До зустрічі!")
            break
        if not command:
            continue
        if command in note_commands:
            print(note_commands[command](args, notebook))
        elif command in commands:
            print(commands[command](args, book))
        else:
            print(f"Невірна команда «{command}». Введіть help — подивитися всі команди та приклади.")


if __name__ == "__main__":
    main()

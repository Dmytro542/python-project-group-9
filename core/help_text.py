HELP: dict[str, tuple[str, str]] = {
    "hello": ("hello", "Привітання."),
    "help": ("help [команда]", "Довідка: усі команди або деталі по одній команді."),
    "add": ("add <ім'я> <телефон>", "Додати контакт або телефон до існуючого (телефон — 10 цифр)."),
    "change": ("change <ім'я> <старий_телефон> <новий_телефон>", "Змінити номер телефону контакту."),
    "phone": ("phone <ім'я>", "Показати телефони контакту."),
    "all": ("all", "Показати всі контакти."),
    "add-birthday": ("add-birthday <ім'я> <DD.MM.YYYY>", "Додати день народження контакту."),
    "show-birthday": ("show-birthday <ім'я>", "Показати день народження контакту."),
    "birthdays": ("birthdays [днів]", "Дні народження на найближчі дні (за замовчуванням 7)."),
    "add-email": ("add-email <ім'я> <email>", "Додати email контакту."),
    "show": ("show <ім'я>", "Показати повну інформацію про контакт."),
    "search": ("search <запит>", "Пошук контактів за іменем, телефоном або email."),
    "note-add": ("note-add <заголовок> <текст нотатки>", "Додати нотатку."),
    "note-search": ("note-search [запит]", "Пошук нотаток за текстом; без запиту — показати всі."),
    "note-delete": ("note-delete <id>", "Видалити нотатку за номером id."),
    "note-edit": ("note-edit <id> <новий текст>", "Змінити вміст нотатки за id."),
}


def _format_help_row(cmd: str, usage: str, desc: str) -> str:
    return f"  {usage:<45} — {desc}"


def show_help(args: list[str], commands_info: dict[str, tuple[str, str]] | None = None) -> str:
    info = commands_info or HELP
    if not args:
        contact_cmds = [c for c in info if not c.startswith("note-") and c not in ("help",)]
        note_cmds = ["note-add", "note-search", "note-delete", "note-edit"]
        lines = [
            "Контакти:",
            *(_format_help_row(c, info[c][0], info[c][1]) for c in contact_cmds if c in info),
            "",
            "Блокнот:",
            *(_format_help_row(c, info[c][0], info[c][1]) for c in note_cmds if c in info),
            "",
            "Інше:",
            "  help [команда]   — ця довідка",
            "  close / exit     — вихід з бота",
        ]
        return "\n".join(lines)
    cmd = args[0].lower()
    if cmd not in info:
        return f"Невідома команда «{cmd}». Введіть help без аргументів для списку команд."
    usage, desc = info[cmd]
    return f"  {usage}\n  -> {desc}"

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

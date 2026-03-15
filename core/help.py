from core.theme import MENU_KEY, MENU_OPTION, MUTED, HEADER, TABLE_BORDER, RESET


CONTACTS_HELP: dict[str, tuple[str, str]] = {
    "add": ("add <ім'я> <телефон>", "Додати контакт або телефон до існуючого."),
    "edit": ("edit <ім'я> <старий> <новий>", "Змінити номер телефону."),
    "phone": ("phone <ім'я>", "Показати телефони контакту."),
    "show": ("show <ім'я>", "Повна інформація про контакт."),
    "all": ("all", "Показати всі контакти."),
    "search": ("search <запит>", "Пошук за ім'ям, телефоном або email."),
    "birthday": ("birthday <ім'я> <DD.MM.YYYY>", "Додати день народження."),
    "show-bd": ("show-bd <ім'я>", "Показати день народження."),
    "birthdays": ("birthdays [днів]", "Найближчі дні народження."),
    "email": ("email <ім'я> <email>", "Додати email."),
    "tag": ("tag <ім'я> <тег>", "Додати тег."),
    "edit-tag": ("edit-tag <ім'я> <старий> <новий>", "Змінити тег."),
    "del-tag": ("del-tag <ім'я> <тег>", "Видалити тег."),
}

NOTES_HELP: dict[str, tuple[str, str]] = {
    "add": ("add <заголовок> <текст>", "Додати нотатку."),
    "all": ("all", "Показати всі нотатки."),
    "search": ("search [запит]", "Пошук нотаток за текстом."),
    "search-tag": ("search-tag <#тег>", "Пошук за тегом."),
    "sort-tag": ("sort-tag", "Сортувати за тегами."),
    "sort-date": ("sort-date [desc]", "Сортувати за датою."),
    "delete": ("delete <id>", "Видалити нотатку."),
    "edit": ("edit <id> <новий текст>", "Редагувати нотатку."),
}


def _format_row(usage: str, desc: str) -> str:
    return f"  {MENU_KEY}{usage:<38}{RESET} {MUTED}{desc}{RESET}"


def show_help(mode: str, args: list[str]) -> str:
    """Показує довідку для поточного режиму."""
    help_dict = CONTACTS_HELP if mode == "contacts" else NOTES_HELP
    mode_name = "Контакти" if mode == "contacts" else "Нотатки"

    if args:
        cmd = args[0].lower()
        if cmd in help_dict:
            usage, desc = help_dict[cmd]
            return f"  {MENU_KEY}{usage}{RESET}\n  {MUTED}{desc}{RESET}"
        return f"{MUTED}Невідома команда «{cmd}». Введіть help для списку.{RESET}"

    lines = [
        f"\n  {HEADER}{mode_name}:{RESET}",
        f"  {TABLE_BORDER}{'─' * 38}{RESET}",
    ]
    for cmd in help_dict:
        usage, desc = help_dict[cmd]
        lines.append(_format_row(usage, desc))

    lines.append(f"\n  {HEADER}Навігація:{RESET}")
    lines.append(f"  {TABLE_BORDER}{'─' * 38}{RESET}")
    lines.append(_format_row("help [команда]", "Ця довідка."))
    lines.append(_format_row("back", "Повернутись в меню."))
    lines.append(_format_row("exit", "Вихід з програми."))

    return "\n".join(lines)

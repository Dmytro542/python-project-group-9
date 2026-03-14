from core.parser import parse_input
from core.completion import get_command_matches, read_line_with_completion
from core.theme import (
    MENU_TITLE, MENU_KEY, MENU_OPTION, RESET,
    SUCCESS, ERROR, WARNING, INFO,
    success, error, warning, info, header,
)
from contacts.storage import load_data, save_data as save_contacts
from contacts import handlers as contact_handlers
from notebook.storage import load_data as load_notebook, save_data as save_notebook
from notebook.handlers import note_add, note_search, note_delete, note_edit, note_sort
from core.help_text import HELP, _format_help_row, show_help
from core.theme import HEADER, MUTED


_ERROR_KEYWORDS = ("не знайдено", "невірн", "помилка", "неправильн", "не існує", "відсутн")
_SUCCESS_KEYWORDS = ("додано", "оновлено", "видалено", "змінено", "збережено", "встановлено")


def _print_result(result: str) -> None:
    """Smart output coloring based on content."""
    if not result:
        return
    text = result.strip()
    if text.startswith("+") or text.startswith("\033"):
        print(result)
        return
    lower = text.lower()
    if any(kw in lower for kw in _ERROR_KEYWORDS):
        print(error(text))
    elif any(kw in lower for kw in _SUCCESS_KEYWORDS):
        print(success(text))
    else:
        print(info(text))


def _register_commands():
    commands = {
        "hello": contact_handlers.hello,
        "help": contact_handlers.help_cmd,
        "add": contact_handlers.add_contact,
        "change": contact_handlers.change_contact,
        "phone": contact_handlers.show_phone,
        "all": contact_handlers.show_all,
        "add-birthday": contact_handlers.add_birthday,
        "show-birthday": contact_handlers.show_birthday,
        "birthdays": contact_handlers.birthdays,
        "show-birthdays": contact_handlers.birthdays,
        "add-email": contact_handlers.add_email,
        "add-address": contact_handlers.add_address,
        "show": contact_handlers.show_contact,
        "search": contact_handlers.search_contact,
        "delete": contact_handlers.delete_contact,
    }
    note_commands = {
        "note-add": note_add,
        "note-search": note_search,
        "note-delete": note_delete,
        "note-edit": note_edit,
        "note-sort": note_sort,
    }
    return {**commands, **note_commands}, commands, note_commands


def _show_contacts_help() -> None:
    contact_cmds = [c for c in HELP if not c.startswith("note-") and c != "help"]
    lines = [
        f"\n{HEADER}Команди адресної книги:{RESET}",
        *(_format_help_row(c, HELP[c][0], HELP[c][1]) for c in contact_cmds if c in HELP),
        f"  {INFO}{'back':<45}{RESET} — {MUTED}повернутись у головне меню{RESET}",
    ]
    print("\n".join(lines))


def _show_notes_help() -> None:
    note_cmds = ["note-add", "note-search", "note-delete", "note-edit", "note-sort"]
    lines = [
        f"\n{HEADER}Команди нотаток:{RESET}",
        *(_format_help_row(c, HELP[c][0], HELP[c][1]) for c in note_cmds if c in HELP),
        f"  {INFO}{'back':<45}{RESET} — {MUTED}повернутись у головне меню{RESET}",
    ]
    print("\n".join(lines))


def _banner():
    title = "Бот-помічник SMART TEAM-9"
    width = len(title) + 6
    print(f"\n{MENU_TITLE}╔{'═' * width}╗{RESET}")
    print(f"{MENU_TITLE}║{RESET}   {header(title)}   {MENU_TITLE}║{RESET}")
    print(f"{MENU_TITLE}╚{'═' * width}╝{RESET}")


def _main_menu_prompt():
    print(f"\n{MENU_TITLE}--- Головне меню ---{RESET}")
    print(f"  {MENU_KEY}1{RESET} — {MENU_OPTION}Адресна книга{RESET}")
    print(f"  {MENU_KEY}2{RESET} — {MENU_OPTION}Нотатки{RESET}")
    print(f"  {MENU_KEY}0{RESET} — {MENU_OPTION}Вихід{RESET}")
    return read_line_with_completion("Оберіть пункт: ", ["1", "2", "0"]).strip()


def main() -> None:
    try:
        from core.intro import play_intro
        play_intro()
    except Exception:
        pass

    book = load_data()
    notebook = load_notebook()
    all_commands, commands, note_commands = _register_commands()
    contact_names = list(commands.keys()) + ["back"]
    note_names = list(note_commands.keys()) + ["back"]

    _banner()
    while True:
        choice = _main_menu_prompt()
        if choice == "0":
            save_contacts(book)
            save_notebook(notebook)
            print(f"\n{SUCCESS}[OK] До зустрічi!{RESET}")
            break
        if choice == "1":
            _show_contacts_help()
            while True:
                user_input = read_line_with_completion("Адресна книга > ", contact_names)
                command, args = parse_input(user_input)
                if command == "back":
                    break
                if not command:
                    continue
                if command in commands:
                    _print_result(commands[command](args, book))
                else:
                    hints = get_command_matches(command, list(commands.keys()))
                    if hints:
                        print(warning(f"Невірна команда «{command}». Можливі: {', '.join(hints)}, back"))
                    else:
                        print(warning(f"Невірна команда «{command}». Введіть help — список команд, back — у меню."))
            continue
        if choice == "2":
            _show_notes_help()
            while True:
                user_input = read_line_with_completion("Нотатки > ", note_names)
                command, args = parse_input(user_input)
                if command == "back":
                    break
                if not command:
                    continue
                if command in note_commands:
                    _print_result(note_commands[command](args, notebook))
                else:
                    hints = get_command_matches(command, list(note_commands.keys()))
                    if hints:
                        print(warning(f"Невірна команда «{command}». Можливі: {', '.join(hints)}, back"))
                    else:
                        print(warning(f"Невірна команда «{command}». Введіть back — у меню."))
            continue
        print(warning("Оберіть 1, 2 або 0."))


if __name__ == "__main__":
    main()

from core.parser import parse_input
from core.completion import get_command_matches, read_line_with_completion
from contacts.storage import load_data, save_data as save_contacts
from contacts import handlers as contact_handlers
from notebook.storage import load_data as load_notebook, save_data as save_notebook
from notebook.handlers import note_add, note_search, note_delete, note_edit, note_sort


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


def _main_menu_prompt():
    print("\n--- Головне меню ---")
    print("  1 — Адресна книга")
    print("  2 — Нотатки")
    print("  0 — Вихід")
    return read_line_with_completion("Оберіть пункт: ", ["1", "2", "0"]).strip()


def main() -> None:
    book = load_data()
    notebook = load_notebook()
    all_commands, commands, note_commands = _register_commands()
    contact_names = list(commands.keys()) + ["back"]
    note_names = list(note_commands.keys()) + ["back"]

    print("Вітаю до бота-помічника!")
    while True:
        choice = _main_menu_prompt()
        if choice == "0":
            save_contacts(book)
            save_notebook(notebook)
            print("До зустрічі!")
            break
        if choice == "1":
            while True:
                user_input = read_line_with_completion("Адресна книга > ", contact_names)
                command, args = parse_input(user_input)
                if command == "back":
                    break
                if not command:
                    continue
                if command in commands:
                    print(commands[command](args, book))
                else:
                    hints = get_command_matches(command, list(commands.keys()))
                    if hints:
                        print(f"Невірна команда «{command}». Можливі: {', '.join(hints)}, back")
                    else:
                        print(f"Невірна команда «{command}». Введіть help — список команд, back — у меню.")
            continue
        if choice == "2":
            while True:
                user_input = read_line_with_completion("Нотатки > ", note_names)
                command, args = parse_input(user_input)
                if command == "back":
                    break
                if not command:
                    continue
                if command in note_commands:
                    print(note_commands[command](args, notebook))
                else:
                    hints = get_command_matches(command, list(note_commands.keys()))
                    if hints:
                        print(f"Невірна команда «{command}». Можливі: {', '.join(hints)}, back")
                    else:
                        print(f"Невірна команда «{command}». Введіть back — у меню.")
            continue
        print("Оберіть 1, 2 або 0.")


if __name__ == "__main__":
    main()

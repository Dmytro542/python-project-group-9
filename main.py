from core.parser import parse_input
from contacts.storage import load_data, save_data as save_contacts
from contacts import handlers as contact_handlers
from notebook.storage import load_data as load_notebook, save_data as save_notebook
from notebook.handlers import note_add, note_search, note_delete, note_edit


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
        "add-email": contact_handlers.add_email,
        "show": contact_handlers.show_contact,
        "search": contact_handlers.search_contact,
    }
    note_commands = {
        "note-add": note_add,
        "note-search": note_search,
        "note-delete": note_delete,
        "note-edit": note_edit,
    }
    return {**commands, **note_commands}, commands, note_commands


def main() -> None:
    book = load_data()
    notebook = load_notebook()
    all_commands, commands, note_commands = _register_commands()

    print("Вітаю до бота-помічника!")
    while True:
        user_input = input("Введіть команду: ")
        command, args = parse_input(user_input)

        if command in ("close", "exit"):
            save_contacts(book)
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

from contacts.storage import load_data as load_contacts, save_data as save_contacts
from contacts.handlers import (
    parse_input, add_contact, change_contact, show_phone,
    show_all, add_birthday, add_email, show_birthday, show_contact,
    birthdays, search_contact, add_tag_to_contact, edit_tag_of_contact,
    remove_tag_from_contact,
)
from contacts.help import show_help
from notebook.storage import load_data as load_notebook, save_data as save_notebook
from notebook.handlers import (
    note_add, note_search, note_delete, note_edit,
    note_search_tag, note_sort_by_tag, note_sort_by_date,
)


def main() -> None:
    """Головний цикл бота з адресною книгою та блокнотом."""
    try:
        from core.intro import play_intro
        play_intro()
    except Exception:
        pass

    book = load_contacts()
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
        "search": search_contact,
        "add-email": add_email,
        "show": show_contact,
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
            save_contacts(book)
            save_notebook(notebook)
            print("\nДо зустрічі!")
            break
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

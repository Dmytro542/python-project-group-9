from contacts.storage import load_data as load_contacts, save_data as save_contacts
from contacts.handlers import (
    add_contact, change_contact, show_phone,
    show_all, add_birthday, add_email, show_birthday, show_contact,
    birthdays, search_contact, add_tag_to_contact, edit_tag_of_contact,
    remove_tag_from_contact,
)
from notebook.storage import load_data as load_notebook, save_data as save_notebook
from notebook.handlers import (
    note_add, note_all, note_search, note_delete, note_edit,
    note_search_tag, note_sort_by_tag, note_sort_by_date,
    note_add_tag, note_del_tag,
)
from core.utils import parse_input
from core.help import show_help
from core.theme import render_menu, mode_header, info, clear_screen


CONTACTS_COMMANDS = {
    "add": add_contact,
    "edit": change_contact,
    "phone": show_phone,
    "show": show_contact,
    "all": show_all,
    "search": search_contact,
    "birthday": add_birthday,
    "show-bd": show_birthday,
    "birthdays": birthdays,
    "email": add_email,
    "tag": add_tag_to_contact,
    "edit-tag": edit_tag_of_contact,
    "del-tag": remove_tag_from_contact,
}

NOTES_COMMANDS = {
    "add": note_add,
    "all": note_all,
    "search": note_search,
    "search-tag": note_search_tag,
    "sort-tag": note_sort_by_tag,
    "sort-date": note_sort_by_date,
    "delete": note_delete,
    "edit": note_edit,
    "add-tag": note_add_tag,
    "del-tag": note_del_tag,
}

CONTACTS_MUTATING = {"add", "edit", "birthday", "email", "tag", "edit-tag", "del-tag"}
NOTES_MUTATING = {"add", "delete", "edit", "add-tag", "del-tag"}


def _save_all(book, notebook):
    save_contacts(book)
    save_notebook(notebook)


def _show_main_menu():
    print(render_menu("Smart Contact Assistant SMART TEAM", [
        ("1", "Контакти"),
        ("2", "Нотатки"),
        ("about", "Про програму"),
        ("exit", "Вихід"),
    ]))


def main() -> None:
    """Головний цикл бота з режимами навігації."""
    try:
        from core.intro import play_intro
        play_intro()
    except Exception:
        pass

    book = load_contacts()
    notebook = load_notebook()

    try:
        from prompt_helper import prompt_input
    except ImportError:
        prompt_input = None

    mode = "main"

    while True:
        try:
            if mode == "main":
                _show_main_menu()
                try:
                    if prompt_input:
                        choice = prompt_input("main").strip().lower()
                    else:
                        choice = input("  Оберіть: ").strip().lower()
                except (KeyboardInterrupt, EOFError):
                    _save_all(book, notebook)
                    print(info("\nДо зустрічі!"))
                    break

                if choice in ("1", "contacts"):
                    mode = "contacts"
                    print(mode_header("Контакти"))
                elif choice in ("2", "notes"):
                    mode = "notes"
                    print(mode_header("Нотатки"))
                elif choice == "about":
                    from core.about import show_about
                    show_about()
                elif choice == "exit":
                    _save_all(book, notebook)
                    print(info("До зустрічі!"))
                    break
                continue

            # --- Режим: контакти або нотатки ---
            try:
                if prompt_input:
                    user_input = prompt_input(mode)
                else:
                    prompt_text = "[Контакти] >>> " if mode == "contacts" else "[Нотатки] >>> "
                    user_input = input(prompt_text)
            except (KeyboardInterrupt, EOFError):
                _save_all(book, notebook)
                print(info("\nДо зустрічі!"))
                break

            command, args = parse_input(user_input)

            if not command:
                continue

            if command == "exit":
                _save_all(book, notebook)
                print(info("До зустрічі!"))
                break

            if command == "back":
                mode = "main"
                clear_screen()
                continue

            if command == "help":
                print(show_help(mode, args))
                continue

            if mode == "contacts":
                if command in CONTACTS_COMMANDS:
                    print(CONTACTS_COMMANDS[command](args, book))
                    if command in CONTACTS_MUTATING:
                        save_contacts(book)
                else:
                    print(info(f"Невідома команда «{command}». Введіть help."))

            elif mode == "notes":
                if command in NOTES_COMMANDS:
                    print(NOTES_COMMANDS[command](args, notebook))
                    if command in NOTES_MUTATING:
                        save_notebook(notebook)
                else:
                    print(info(f"Невідома команда «{command}». Введіть help."))

        except Exception as e:
            print(f"Помилка: {e}")


if __name__ == "__main__":
    main()

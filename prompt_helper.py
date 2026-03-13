"""Автодоповнення команд та підказки полів для CLI-бота."""

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.document import Document


# Опис аргументів для кожної команди: список підказок для кожного поля
COMMAND_ARGS: dict[str, list[str]] = {
    "hello": [],
    "help": ["[команда]"],
    "add": ["<ім'я>", "<телефон>"],
    "change": ["<ім'я>", "<старий_телефон>", "<новий_телефон>"],
    "phone": ["<ім'я>"],
    "all": [],
    "add-birthday": ["<ім'я>", "<DD.MM.YYYY>"],
    "show-birthday": ["<ім'я>"],
    "show-birthdays": ["[кількість_днів]"],
    "search": ["<запит>"],
    "add-email": ["<ім'я>", "<email>"],
    "show": ["<ім'я>"],
    "note-add": ["<заголовок>", "<текст нотатки>"],
    "note-search": ["[запит]"],
    "note-search-tag": ["<#тег>"],
    "note-sort-tag": [],
    "note-sort-date": ["[desc]"],
    "note-delete": ["<id>"],
    "note-edit": ["<id>", "<новий текст>"],
    "close": [],
    "exit": [],
}

ALL_COMMANDS = list(COMMAND_ARGS.keys())


class CommandCompleter(Completer):
    """Доповнює команди та показує підказки полів."""

    def get_completions(self, document: Document, complete_event):
        text = document.text_before_cursor
        parts = text.split()

        # Якщо нічого не введено або вводимо перше слово (без пробілу) — підказуємо команди
        if not parts or (len(parts) == 1 and not text.endswith(" ")):
            word = parts[0].lower() if parts else ""
            for cmd in ALL_COMMANDS:
                if cmd.startswith(word):
                    yield Completion(cmd, start_position=-len(word))
        else:
            # Команда вже введена — підказуємо яке поле зараз очікується
            cmd = parts[0].lower()
            if cmd in COMMAND_ARGS:
                arg_hints = COMMAND_ARGS[cmd]
                # Визначаємо індекс поточного аргументу
                # Якщо текст закінчується пробілом — наступний аргумент
                # Якщо ні — поточний (ще вводиться)
                if text.endswith(" "):
                    arg_index = len(parts) - 1
                else:
                    arg_index = len(parts) - 2

                if 0 <= arg_index < len(arg_hints):
                    hint = arg_hints[arg_index]
                    # Показуємо підказку як placeholder (не замінює введений текст)
                    yield Completion(hint, start_position=0, display_meta="поле")


def _create_session() -> PromptSession:
    """Створює PromptSession з обробкою помилок для різних терміналів."""
    import sys

    kwargs = dict(
        completer=CommandCompleter(),
        complete_while_typing=True,
        complete_in_thread=True,
    )

    # На Windows у деяких терміналах (Git Bash, IDE terminals) Win32Output
    # не працює — пробуємо Vt100Output як fallback
    if sys.platform == "win32":
        try:
            return PromptSession(**kwargs)
        except Exception:
            try:
                from prompt_toolkit.output.vt100 import Vt100_Output
                output = Vt100_Output(sys.stdout)
                return PromptSession(output=output, **kwargs)
            except Exception:
                return None
    else:
        return PromptSession(**kwargs)


# Створюємо сесію один раз при імпорті
_session: PromptSession | None = None
_session_initialized = False


def prompt_input() -> str:
    """Запитує введення користувача з автодоповненням."""
    global _session, _session_initialized

    if not _session_initialized:
        _session_initialized = True
        try:
            _session = _create_session()
        except Exception:
            _session = None

    if _session is not None:
        try:
            def _show_completions():
                # Відкриваємо меню автодоповнення одразу при появі промпту
                buf = _session.app.current_buffer
                buf.start_completion()

            return _session.prompt("Введіть команду: ", pre_run=_show_completions)
        except Exception:
            # Якщо prompt_toolkit зламався під час роботи — fallback
            _session = None

    return input("Введіть команду: ")

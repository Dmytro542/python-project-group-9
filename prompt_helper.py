"""Автодоповнення команд та підказки полів для CLI-бота (з підтримкою режимів)."""

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.document import Document
from prompt_toolkit.formatted_text import ANSI


COMMAND_ARGS_BY_MODE: dict[str, dict[str, list[str]]] = {
    "main": {
        "contacts": [],
        "notes": [],
        "exit": [],
        "close": [],
    },
    "contacts": {
        "add": ["<ім'я>", "<телефон>"],
        "edit": ["<ім'я>", "<старий_телефон>", "<новий_телефон>"],
        "phone": ["<ім'я>"],
        "show": ["<ім'я>"],
        "all": [],
        "search": ["<запит>"],
        "birthday": ["<ім'я>", "<DD.MM.YYYY>"],
        "show-bd": ["<ім'я>"],
        "birthdays": ["[кількість_днів]"],
        "email": ["<ім'я>", "<email>"],
        "tag": ["<ім'я>", "<тег>"],
        "edit-tag": ["<ім'я>", "<старий>", "<новий>"],
        "del-tag": ["<ім'я>", "<тег>"],
        "help": ["[команда]"],
        "back": [],
        "exit": [],
    },
    "notes": {
        "add": ["<заголовок>", "<текст>"],
        "search": ["[запит]"],
        "search-tag": ["<#тег>"],
        "sort-tag": [],
        "sort-date": ["[desc]"],
        "delete": ["<id>"],
        "edit": ["<id>", "<новий текст>"],
        "help": ["[команда]"],
        "back": [],
        "exit": [],
    },
}

_current_mode = "contacts"


class CommandCompleter(Completer):
    """Доповнює команди та показує підказки полів залежно від режиму."""

    def get_completions(self, document: Document, complete_event):
        commands = COMMAND_ARGS_BY_MODE.get(_current_mode, {})
        text = document.text_before_cursor
        parts = text.split()

        if not parts or (len(parts) == 1 and not text.endswith(" ")):
            word = parts[0].lower() if parts else ""
            for cmd in commands:
                if cmd.startswith(word):
                    yield Completion(cmd, start_position=-len(word))
        else:
            cmd = parts[0].lower()
            if cmd in commands:
                arg_hints = commands[cmd]
                if text.endswith(" "):
                    arg_index = len(parts) - 1
                else:
                    arg_index = len(parts) - 2

                if 0 <= arg_index < len(arg_hints):
                    hint = arg_hints[arg_index]
                    yield Completion(hint, start_position=0, display_meta="поле")


def _create_session() -> PromptSession:
    """Створює PromptSession з обробкою помилок для різних терміналів."""
    import sys

    kwargs = dict(
        completer=CommandCompleter(),
        complete_while_typing=True,
        complete_in_thread=True,
    )

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


_session: PromptSession | None = None
_session_initialized = False

_MODE_PROMPTS = {
    "main": "  Оберіть: ",
    "contacts": "\033[93;1m[Контакти]\033[0m >>> ",
    "notes": "\033[93;1m[Нотатки]\033[0m >>> ",
}


def prompt_input(mode: str = "contacts") -> str:
    """Запитує введення користувача з автодоповненням для вказаного режиму."""
    global _session, _session_initialized, _current_mode

    _current_mode = mode

    if not _session_initialized:
        _session_initialized = True
        try:
            _session = _create_session()
        except Exception:
            _session = None

    prompt_text = _MODE_PROMPTS.get(mode, ">>> ")

    if _session is not None:
        try:
            def _show_completions():
                buf = _session.app.current_buffer
                buf.start_completion()

            return _session.prompt(ANSI(prompt_text), pre_run=_show_completions)
        except Exception:
            _session = None

    return input(prompt_text)

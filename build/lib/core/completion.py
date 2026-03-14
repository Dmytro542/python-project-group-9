def get_command_matches(prefix: str, command_names: list[str]) -> list[str]:
    if not prefix:
        return []
    lower = prefix.lower()
    return sorted(c for c in command_names if c.startswith(lower))


def _command_completer(command_names: list[str]):
    from prompt_toolkit.completion import Completer, Completion

    class _FirstWordCompleter(Completer):
        def get_completions(self, document, complete_event):
            text_before = document.text_before_cursor
            if " " in text_before:
                return
            prefix = text_before.lower()
            for cmd in sorted(command_names):
                if cmd.startswith(prefix):
                    yield Completion(cmd, start_position=-len(prefix))

    return _FirstWordCompleter()


def read_line_with_completion(prompt_text: str, command_names: list[str]) -> str:
    try:
        from prompt_toolkit import prompt
        from prompt_toolkit.formatted_text import HTML
        completer = _command_completer(command_names)
        styled_prompt = HTML(f"<b><yellow>{prompt_text}</yellow></b>")
        return prompt(styled_prompt, completer=completer)
    except ImportError:
        return input(prompt_text)
    except Exception as e:
        if type(e).__name__ == "NoConsoleScreenBufferError":
            return input(prompt_text)
        raise

from core.theme import error, warning


def input_error(func):
    """Декоратор обробляє KeyError, ValueError, IndexError у handler-функціях."""

    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return error("Контакт не знайдено.")
        except ValueError as e:
            return error(str(e)) if str(e) else error("Невірний формат даних.")
        except IndexError:
            return warning("Вкажіть усі аргументи для команди.")

    return inner


def parse_input(user_input: str) -> tuple[str | None, list[str]]:
    """Розбиває введений рядок на команду та список аргументів."""
    parts = user_input.strip().split()
    if not parts:
        return None, []
    return parts[0].lower(), parts[1:]

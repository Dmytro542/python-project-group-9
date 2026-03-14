import re


def validate_email(value: str) -> tuple[bool, str]:
    """
    Перевіряє чи є рядок коректним email.
    Повертає (True, "") якщо валідний, або (False, "причина") якщо ні.
    """
    # Порожнє значення
    if not value:
        return False, "Email не може бути порожнім."

    # Пробіли
    if " " in value:
        return False, "Email не може містити пробіли."

    # Кирилиця
    if re.search(r"[а-яёіїєґА-ЯЁІЇЄҐ]", value):
        return False, "Email не може містити кириличні літери."

    # Перевірка наявності @
    if "@" not in value:
        return False, "Email має містити символ @."

    local, _, domain = value.partition("@")

    # Порожня локальна частина (перед @)
    if not local:
        return False, "Email не може починатись з @."

    # Крапка на початку локальної частини
    if local.startswith("."):
        return False, "Email не може починатись з крапки."

    # Крапка в кінці локальної частини або всього email
    if local.endswith(".") or value.endswith("."):
        return False, "Email не може закінчуватись крапкою."

    # Подвійна крапка
    if ".." in value:
        return False, "Email не може містити подвійну крапку."

    # Крапка одразу після @
    if domain.startswith("."):
        return False, "Домен не може починатись з крапки."

    # Відсутність крапки в домені
    if "." not in domain:
        return False, "Домен має містити крапку (наприклад: gmail.com)."

    # Загальна перевірка формату
    pattern = r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$"
    if not re.match(pattern, value):
        return False, "Невірний формат email. Приклад: user@example.com"

    return True, ""

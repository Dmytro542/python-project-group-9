class Field:
    """Базовый класс для полей записи в адресной книге."""

    def __init__(self, value):
        self.value = value

    def __str__(self) -> str:
        return str(self.value)
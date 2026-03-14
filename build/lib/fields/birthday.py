from datetime import datetime, date
from .base_field import Field


class Birthday(Field):
    """Поле дня народження. Формат: DD.MM.YYYY"""

    def __init__(self, value):
        try:
            if isinstance(value, date):
                self._value = value
            else:
                self._value = datetime.strptime(str(value), "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Невірний формат дати. Використовуйте DD.MM.YYYY.")

    @property
    def value(self):
        return self._value

    def __str__(self):
        return self._value.strftime("%d.%m.%Y")
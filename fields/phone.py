from .base_field import Field


class Phone(Field):
    """Поле для зберігання номера телефону. Валідація: 10 цифр."""

    def __init__(self, value):
        if not self._is_valid(value):
            raise ValueError("Номер телефону має містити рівно 10 цифр.")
        super().__init__(value)

    @staticmethod
    def _is_valid(value):
        digits = "".join(c for c in str(value) if c.isdigit())
        return len(digits) == 10
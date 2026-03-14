from .base_field import Field
from .email_validator import validate_email


class Email(Field):
    """Поле для зберігання email контакту з валідацією."""

    def __init__(self, value: str):
        is_valid, error = validate_email(value)
        if not is_valid:
            raise ValueError(error)
        super().__init__(value)

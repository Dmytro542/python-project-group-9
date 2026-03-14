from datetime import date, timedelta
from .Utils import birthday_in_year


def get_upcoming_birthdays(book, upcoming_days: int) -> list[dict[str, str]]:
    today = date.today()
    result = []
    for record in book.data.values():
        if record.birthday is None:
            continue
        birth = record.birthday.value
        birthday_this_year = birthday_in_year(birth, today.year)
        delta_days = (birthday_this_year - today).days
        if delta_days < 0:
            birthday_this_year = birthday_in_year(birth, today.year + 1)
            delta_days = (birthday_this_year - today).days
        if 0 <= delta_days <= upcoming_days:
            congratulation_date = birthday_this_year
            if congratulation_date.weekday() == 5:
                congratulation_date += timedelta(days=2)
            elif congratulation_date.weekday() == 6:
                congratulation_date += timedelta(days=1)
            result.append({
                "name": record.name.value,
                "congratulation_date": congratulation_date.strftime("%d.%m.%Y"),
            })
    return result
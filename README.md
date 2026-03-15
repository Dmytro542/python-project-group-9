# Персональний помічник

Термінальний бот для управління контактами та нотатками з підтримкою пошуку, сортування, тегів та збереження даних між сесіями.

## Вимоги

- Python 3.11+
- colorama
- prompt_toolkit >= 3.0

## Встановлення та запуск

### Windows

```bash
run.bat
```

### Linux / macOS

```bash
bash run.sh
```

### Вручну

```bash
python3.11 -m venv .venv
source .venv/bin/activate        # Linux/macOS
# .venv\Scripts\activate         # Windows
pip install -r requirements.txt
python main.py
```

## Команди

Після запуску бот пропонує головне меню з вибором режиму: **Контакти**, **Нотатки** або **Вихід**.

### Контакти

| Команда | Синтаксис | Опис |
|---|---|---|
| `add` | `add <ім'я> <телефон>` | Додати контакт або телефон до існуючого |
| `edit` | `edit <ім'я> <старий тел> <новий тел>` | Змінити номер телефону |
| `phone` | `phone <ім'я>` | Показати телефони контакту |
| `show` | `show <ім'я>` | Показати повну інформацію про контакт |
| `all` | `all` | Показати всі контакти у таблиці |
| `search` | `search <запит>` | Пошук за іменем, телефоном або email |
| `birthday` | `birthday <ім'я> <DD.MM.YYYY>` | Додати день народження |
| `show-bd` | `show-bd <ім'я>` | Показати день народження |
| `birthdays` | `birthdays [кількість днів]` | Найближчі дні народження (за замовч. 7 днів) |
| `email` | `email <ім'я> <email>` | Додати email |
| `tag` | `tag <ім'я> <тег>` | Додати тег до контакту |
| `edit-tag` | `edit-tag <ім'я> <старий> <новий>` | Змінити тег |
| `del-tag` | `del-tag <ім'я> <тег>` | Видалити тег |
| `delete` | `delete <ім'я>` | Видалити контакт |

### Нотатки

| Команда | Синтаксис | Опис |
|---|---|---|
| `add` | `add <заголовок> <текст>` | Додати нотатку |
| `all` | `all` | Показати всі нотатки |
| `search` | `search [запит]` | Пошук нотаток за текстом |
| `search-tag` | `search-tag <#тег>` | Пошук нотаток за тегом |
| `sort-tag` | `sort-tag` | Сортувати нотатки за тегами |
| `sort-date` | `sort-date [desc]` | Сортувати за датою створення |
| `edit` | `edit <id> <новий текст>` | Змінити вміст нотатки |
| `delete` | `delete <id>` | Видалити нотатку за id |

### Загальні

| Команда | Опис |
|---|---|
| `help` | Список доступних команд |
| `back` | Повернутися до головного меню |
| `exit` / `close` | Вийти з програми |

## Структура проєкту

```
├── main.py                    # Точка входу, головний цикл
├── prompt_helper.py           # Автодоповнення команд (prompt_toolkit)
├── requirements.txt           # Залежності
├── run.sh / run.bat           # Скрипти запуску
│
├── core/
│   ├── utils.py               # parse_input(), декоратор @input_error
│   ├── help.py                # Система довідки
│   ├── theme.py               # Кольори, таблиці, меню (colorama)
│   └── intro.py               # Matrix-анімація при запуску
│
├── contacts/
│   ├── models.py              # Record, AddressBook
│   ├── handlers.py            # Обробники команд контактів
│   ├── storage.py             # Збереження у JSON
│   └── birthdays.py           # Логіка днів народження
│
├── notebook/
│   ├── models.py              # Модель Note
│   ├── notebook.py            # CRUD операції
│   ├── handlers.py            # Обробники команд нотаток
│   ├── search.py              # Пошук і сортування
│   └── storage.py             # Збереження у JSON
│
├── fields/
│   ├── base_field.py          # Базовий клас поля
│   ├── name.py                # Поле імені
│   ├── phone.py               # Поле телефону (10 цифр)
│   ├── birthday.py            # Поле дня народження (DD.MM.YYYY)
│   ├── email.py               # Поле email
│   └── email_validator.py     # Валідація email
│
└── data/
    ├── contacts.json          # Збережені контакти
    └── notebook.json          # Збережені нотатки
```

## Збереження даних

Дані зберігаються автоматично у форматі JSON у папці `data/`:
- `contacts.json` — контакти
- `notebook.json` — нотатки

Дані не втрачаються між перезапусками програми.

## Автори

TEAM-9:

- Mykhailo Kachanov
- Oksana Khomenko
- Oleksandr Sluch
- Dmytro Rubakhin

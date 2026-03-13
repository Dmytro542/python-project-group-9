def contacts_table(records, include_address=True):
    from prettytable import PrettyTable
    headers = ["Ім'я", "Телефони", "Email", "День народження"]
    if include_address:
        headers.insert(3, "Адреса")
    table = PrettyTable(headers)
    for record in records:
        phones_str = ", ".join(p.value for p in record.phones) if record.phones else "—"
        email_str = record.email.value if getattr(record, "email", None) and record.email else "—"
        birthday_str = str(record.birthday) if record.birthday else "—"
        address_str = record.address if getattr(record, "address", None) and record.address else "—"
        row = [record.name.value, phones_str, email_str]
        if include_address:
            row.append(address_str)
        row.append(birthday_str)
        table.add_row(row)
    return table.get_string()


def notes_table(notes, tag_header="Теги"):
    from prettytable import PrettyTable
    headers = ["ID", "Заголовок", "Зміст", tag_header]
    table = PrettyTable(headers)
    for note in notes:
        tags_val = getattr(note, "tags", None)
        tags_str = ", ".join(tags_val) if tags_val else "—"
        content_short = (note.content[:50] + "…") if len(note.content) > 50 else note.content
        table.add_row([note.id, note.title, content_short, tags_str])
    return table.get_string()

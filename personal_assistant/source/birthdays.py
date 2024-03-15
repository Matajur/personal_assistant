"""Module providing a function to display a list of colleagues with upcoming birthdays"""

from datetime import datetime, timedelta, date

from source.classes import AddressBook, Record, SPAN, COLUMN_1, COLUMN_2, COLUMN_3, COLUMN_4, COLUMN_5, COLUMN_6  # noqa

FIELD = SPAN - COLUMN_1 - 1
SEPARATOR = "-" * (SPAN + 2)
INDENT = " " * COLUMN_1
HEADER = f"|{'#':^{COLUMN_1}}|{'FULLNAME':^{COLUMN_2}}|{'EMAIL':^{COLUMN_3}}|{'PHONES':^{COLUMN_4}}|{'BIRTHDAY':^{COLUMN_5}}|{'ADDRESS':^{COLUMN_6}}|"
SKIPPER = f"|{INDENT}|{'Operation skipped':<{FIELD}}|"


def search_upcoming_birthday_contacts(book: AddressBook, *_) -> None:
    if not len(book):
        print(SEPARATOR)
        print(f"|{' ' * COLUMN_1}|{'Contact book is empty':<{FIELD}}|")
        return

    days = get_days()
    today = datetime.now().date()
    end_date = today + timedelta(days=days)
    contacts = []

    for contact in book.values():
        if contact.birthday is not None:
            origin_birthday = contact.birthday.value
            this_year_birthday = datetime(year=today.year, month=origin_birthday.month, day=origin_birthday.day).date()
            if today <= this_year_birthday <= end_date:
                contacts.append(contact)

    show_result(today, end_date, contacts)


def get_days() -> int:
    while True:
        print(SEPARATOR)
        input_value = input(f"|{INDENT}|{'Enter the number of days for which to show birthdays'}: ")
        if input_value.isdigit():
            return int(input_value)

        print(SEPARATOR)
        print(f"|{INDENT}|{'The number must be of integer type only':<{FIELD}}|")


def show_result(start_day: date, end_day: date, result: []) -> None:
    if len(result):
        date_range = start_day.strftime('%d.%m.%Y') + ' - ' + end_day.strftime('%d.%m.%Y')
        print(SEPARATOR)
        print(f"|{INDENT}|{'Birthdays in range ' + date_range:<{FIELD}}|")
        print(SEPARATOR)
        print(HEADER)
        print(SEPARATOR)
        for number, record in enumerate(result):
            print(f"|{number + 1:^{COLUMN_1}}|{record}|")
    else:
        print(SEPARATOR)
        print(f"|{' ' * COLUMN_1}|{'Empty result':<{FIELD}}|")

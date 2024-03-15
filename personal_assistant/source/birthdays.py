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

    handle_contacts(book)


def handle_contacts(book: AddressBook) -> None:
    days = get_days()
    today = datetime.now().date()
    end_date = today + timedelta(days=days)
    contacts = get_contacts(book, today, end_date)

    if len(contacts):
        today_formatted = today.strftime('%d.%m.%Y')
        end_date_formatted = end_date.strftime('%d.%m.%Y')
        print(SEPARATOR)
        print(f"|{INDENT}|{'Birthdays in range ' + today_formatted + ' - ' + end_date_formatted:<{FIELD}}|")
        print(SEPARATOR)
        print(HEADER)
        print(SEPARATOR)
        for number, record in enumerate(contacts):
            print(f"|{number + 1:^{COLUMN_1}}|{record}|")
    else:
        print(SEPARATOR)
        print(f"|{' ' * COLUMN_1}|{'Empty result':<{FIELD}}|")


def get_days() -> int:
    while True:
        print(SEPARATOR)
        input_value = input(f"|{INDENT}|{'Enter the number of days for which to show birthdays'}: ")
        if input_value.isdigit():
            return int(input_value)

        print(SEPARATOR)
        print(f"|{INDENT}|{'The number must be of integer type only':<{FIELD}}|")


def get_contacts(book: AddressBook, today: date, end_date: date) -> []:
    contacts = []
    for contact in book.values():
        if contact.birthday is not None:
            origin_birthday = contact.birthday.value
            this_year_birthday = datetime(year=today.year, month=origin_birthday.month, day=origin_birthday.day).date()
            if today <= this_year_birthday <= end_date:
                contacts.append(contact)
    return contacts

"""Module providing a functionality to manage the contacts in a contact list"""

import re
from datetime import datetime
from typing import Tuple

from source.birthdays import search_upcoming_birthday_contacts  # noqa
from source.classes import (
    BirthdayFormatError,
    BirthdayValidationError,
    NameValidationError,
    PhoneIndexError,
    PhoneValidationError,
    RecordValidationError,
    Record,
    AddressBook,
)
from source.classes import COLUMN_1, COLUMN_2, COLUMN_3, COLUMN_4, COLUMN_5, COLUMN_6, SPAN  # noqa
from source.search_contacts import search_contacts_handler  # noqa

FIELD = SPAN - COLUMN_1 - 1
SEPARATOR = "-" * (SPAN + 2)
INDENT = " " * COLUMN_1
HEADER = f"|{'#':^{COLUMN_1}}|{'FULLNAME':^{COLUMN_2}}|{'EMAIL':^{COLUMN_3}}|{'PHONES':^{COLUMN_4}}|{'BIRTHDAY':^{COLUMN_5}}|{'ADDRESS':^{COLUMN_6}}|"
SKIPPER = f"|{INDENT}|{'Operation skipped':<{FIELD}}|"


def input_error(func) -> str:
    """
    A decorator to handle input errors.

    :param func: function where an input error can occur
    :return: function if no input error occurred, or a description of the error
    """

    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            print(SEPARATOR)
            print(f"|{INDENT}|{'Provide name and phone':<{FIELD}}|")
            return invalid_command
        except KeyError:
            print(SEPARATOR)
            print(f"|{INDENT}|{'Contact not found':<{FIELD}}|")
            return invalid_command
        except IndexError:
            print(SEPARATOR)
            print(f"|{INDENT}|{'Provide contact name':<{FIELD}}|")
            return invalid_command
        except TypeError:
            print(SEPARATOR)
            print(f"|{INDENT}|{'Provide contact name':<{FIELD}}|")
            return invalid_command
        except BirthdayFormatError:
            print(SEPARATOR)
            print(f"|{INDENT}|{'Birthday must be in DD.MM.YYYY format':<{FIELD}}|")
            return invalid_command
        except BirthdayValidationError:
            print(SEPARATOR)
            print(
                f"|{INDENT}|{'Birthday cannot be in future or more than 100 years ago':<{FIELD}}|"
            )
            return invalid_command
        except NameValidationError:
            print(SEPARATOR)
            print(f"|{INDENT}|{'The name must contain 3-20 characters':<{FIELD}}|")
            return invalid_command
        except PhoneIndexError:
            print(SEPARATOR)
            print(
                f"|{INDENT}|{'There is no such phone number in the record':<{FIELD}}|"
            )
            return invalid_command
        except PhoneValidationError:
            print(SEPARATOR)
            print(
                f"|{INDENT}|{'Wrong phone number format, should be 10 digits, ex. 1234567890':<{FIELD}}|"
            )
            return invalid_command
        except RecordValidationError:
            print(SEPARATOR)
            print(f"|{INDENT}|{'A contact with that name already exists':<{FIELD}}|")
            return invalid_command

    return inner


def get_command(command: str):
    """
    A function to map user input to appropriate commands.

    :param command: user input in str format
    :return: function
    """
    commands = {
        "1": show_contacts,
        "2": contact_adder,
        "4": search_contacts_handler,
        "5": search_upcoming_birthday_contacts,
    }

    cmd = commands.get(command)
    if not cmd:
        return invalid_command
    return cmd


@input_error
def contact_adder(book: AddressBook, *_) -> None:
    """
    Function to add new records to contact book

    :param book: a dictionary with user contacts
    :return: None, prints only a message about the success or failure of the operation
    """
    name = name_setter(book)
    if name:
        record = Record(name)

        address_setter(record)
        phone_setter(record)
        if record.phones:
            print(f"|{INDENT}|{'Would you like to add one more phone or press Enter to skip'}: ")
            phone_setter(record)
        email_setter(record)
        birthday_setter(record)

        print(SEPARATOR)
        print(HEADER)
        print(SEPARATOR)
        print(f"|{INDENT}|{record}|")
        print(SEPARATOR)
        print(f"|{'0':^{COLUMN_1}}|{'Skip'}: ")
        print(f"|{'1':^{COLUMN_1}}|{'Save'}: ")
        print(SEPARATOR)
        decision = input(f"|{INDENT}|{'Save changes to contact book'}: ")
        if decision == "1":
            book.add_record(record)
            print(SEPARATOR)
            print(f"|{INDENT}|{'New record added to address book':<{FIELD}}|")
        else:
            print(SEPARATOR)
            print(SKIPPER)


def name_setter(book: AddressBook) -> None | str:
    """
    Function to set record name

    :param book: a dictionary with user contacts
    :return: None or record name
    """
    while True:
        print(SEPARATOR)
        name = input(f"|{INDENT}|{'Enter new record name or 0 to exit'}: ")
        if name == "0":
            print(SEPARATOR)
            print(SKIPPER)
            return None
        if name in book.data.keys():
            print(SEPARATOR)
            print(f"|{INDENT}|{f'Record with name {name} already exists':<{FIELD}}|")
        if 2 < len(name) < 21:
            return name
        print(SEPARATOR)
        print(f"|{INDENT}|{'The name must contain 3-20 characters':<{FIELD}}|")


def address_setter(record: Record) -> None:
    """
    Function to add address to a record

    :param record: a record from contact book
    :return: None
    """
    while True:
        address = input(f"|{INDENT}|{'Enter address or press Enter to skip'}: ")
        if address:
            if 2 < len(address) < 41:
                record.add_address(address)
                break
            print(SEPARATOR)
            print(f"|{INDENT}|{'The address must contain 3-40 characters':<{FIELD}}|")
        break


def phone_setter(record: Record) -> None:
    """
    Function to add phone number to a record

    :param record: a record from contact book
    :return: None
    """
    while True:
        phone = input(f"|{INDENT}|{'Enter phone (ex. +380991234567) or press Enter to skip'}: ")
        if phone:
            if re.match(r"\+\d{12}", phone):
                record.add_phone(phone)
                break
            print(SEPARATOR)
            print(f"|{INDENT}|{'The phone number must have +380991234567 format':<{FIELD}}|")
        else:
            break


def birthday_setter(record: Record) -> None:
    """
    Function to add birthday to a record

    :param record: a record from contact book
    :return: None
    """
    while True:
        birthday = input(f"|{INDENT}|{'Enter birthday (ex. DD.MM.YYYY) or press Enter to skip'}: ")
        if birthday:
            if re.match(r'^(0[1-9]|[1-2][0-9]|3[0-1])\.(0[1-9]|1[0-2])\.\d{4}$', birthday):
                birth = datetime.strptime(birthday, "%d.%m.%Y").date()
                if 0 <= (datetime.today().date() - birth).days <= 100 * 365.4:
                    record.add_birthday(birthday)
                    break
                print(SEPARATOR)
                print(
                    f"|{INDENT}|{'Birthday cannot be in future or more than 100 years ago':<{FIELD}}|"
                )
            print(SEPARATOR)
            print(f"|{INDENT}|{'Birthday must be in DD.MM.YYYY format':<{FIELD}}|")
        else:
            break


def email_setter(record: Record) -> None:
    """
    Function to add email to a record

    :param record: a record from contact book
    :return: None
    """
    while True:
        email = input(f"|{INDENT}|{'Enter email (ex. example@mail.com) or press Enter to skip'}: ")
        if email:
            if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                record.add_email(email)
                break
            print(SEPARATOR)
            print(f"|{INDENT}|{'The email must be in example@mail.com format':<{FIELD}}|")
        else:
            break


def invalid_command(*_) -> None:
    """
    Ivalid command handler.

    :return: None, only prints message about invalid command
    """
    print(SEPARATOR)
    print(f"|{INDENT}|{'Invalid command':<{FIELD}}|")


def show_contacts(book: AddressBook, *_) -> None:
    """
    Function of displaying a complete list of contacts.

    :param book: a dictionary with user contacts
    :return: None, only prints the contact list or a warning that the
            contact list is empty
    """
    if len(book):
        contacts = dict(sorted(book.items()))
        print(SEPARATOR)
        print(HEADER)
        print(SEPARATOR)
        for number, record in enumerate(contacts.values()):
            print(f"|{number + 1:^{COLUMN_1}}|{record}|")

    else:
        print(SEPARATOR)
        print(f"|{' ' * COLUMN_1}|{'Contact book is empty':<{FIELD}}|")


def parse_input(user_input: str) -> Tuple[str, ...]:
    """
    Function to parse commands received from the user using the CLI.

    :param user: a string with a command and possible arguments
    :return cmd, *args: a tuple with a command in string format and
                        the arguments, if any, as a tuple of strings
    """
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

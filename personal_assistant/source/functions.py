"""Module providing a functionality to manage the contacts in a contact list"""

from datetime import datetime

from source.birthdays import get_birthdays_per_week  # noqa
from source.classes import (
    BirthdayFormatError,
    BirthdayValidationError,
    NameValidationError,
    PhoneIndexError,
    PhoneValidationError,
    RecordValidationError,
    Record,
    AddressBook,
    Name,
)
from source.classes import COLUMN_1, COLUMN_2, COLUMN_3, COLUMN_4, COLUMN_5, COLUMN_6

SPAN = COLUMN_1 + COLUMN_2 + COLUMN_3 + COLUMN_4 + COLUMN_5 + COLUMN_6 + 5
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
        except KeyError:
            print(SEPARATOR)
            print(f"|{INDENT}|{'Contact not found':<{FIELD}}|")
        except IndexError:
            print(SEPARATOR)
            print(f"|{INDENT}|{'Provide contact name':<{FIELD}}|")
        except TypeError:
            print(SEPARATOR)
            print(f"|{INDENT}|{'Provide contact name':<{FIELD}}|")
        except BirthdayFormatError:
            print(SEPARATOR)
            print(f"|{INDENT}|{'Birthday must be in DD.MM.YYYY format':<{FIELD}}|")
        except BirthdayValidationError:
            print(SEPARATOR)
            print(
                f"|{INDENT}|{'Birthday cannot be in future or more than 100 years ago':<{FIELD}}|"
            )
        except NameValidationError:
            print(SEPARATOR)
            print(f"|{INDENT}|{'The name must contain 3-20 characters':<{FIELD}}|")
            return(None)
        except PhoneIndexError:
            print(SEPARATOR)
            print(
                f"|{INDENT}|{'There is no such phone number in the record':<{FIELD}}|"
            )
        except PhoneValidationError:
            print(SEPARATOR)
            print(
                f"|{INDENT}|{'Wrong phone number format, should be 10 digits, ex. 1234567890':<{FIELD}}|"
            )
        except RecordValidationError:
            print(SEPARATOR)
            print(f"|{INDENT}|{'A contact with that name already exists':<{FIELD}}|")

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
    }

    cmd = commands.get(command)
    if not cmd:
        return invalid_command
    return cmd


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
        email_setter(record)
        birthday_setter(record)

        print(SEPARATOR)
        print(HEADER)
        print(SEPARATOR)
        print(f"|{INDENT}|{record}|")
        print(SEPARATOR)
        print(f"|{"0":^{COLUMN_1}}|{'Skip'}: ")
        print(f"|{"1":^{COLUMN_1}}|{'Save'}: ")
        print(SEPARATOR)
        decision = input(f"|{INDENT}|{'Save changes to contact book'}: ")
        if decision == "1":
            book.add_record(record)
            print(SEPARATOR)
            print(f"|{INDENT}|{'New record added to address book':<{FIELD}}|")
        else:
            print(SEPARATOR)
            print(SKIPPER)


@input_error
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
            print(f"|{INDENT}|{'Record with name {name} already exists':<{FIELD}}|")
        # name_ = Name(name)
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
            print(f"|{INDENT}|{'The name must contain 3-40 characters':<{FIELD}}|")
        break

def phone_setter(record: Record) -> None:
    """
    Function to add phone number to a record

    :param record: a record from contact book
    :return: None
    """
    while True:
        phone = input(f"|{INDENT}|{'Enter phone (ex. 0991234567) or press Enter to skip'}: ")
        if phone:
            if len(phone) == 10:
                record.add_phone(phone)
                break
            print(SEPARATOR)
            print(f"|{INDENT}|{'The phone number must have 0991234567 format':<{FIELD}}|")
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
            try:
                datetime.strptime(birthday, "%d.%m.%Y").date()
                record.add_birthday(birthday)
                break
            except ValueError:
                print(SEPARATOR)
                print(f"|{INDENT}|{'Birthday must be in DD.MM.YYYY format':<{FIELD}}|")
                continue
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
            if 2 < len(email) < 20:
                record.add_email(email)
                break
            print(SEPARATOR)
            print(f"|{INDENT}|{'The email must contain 3-40 characters':<{FIELD}}|")
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
            print(f"|{number+1:^{COLUMN_1}}|{record}|")

    else:
        print(SEPARATOR)
        print(f"|{' ' * COLUMN_1}|{'Contact book is empty':<{FIELD}}|")


def parse_input(user_input: str) -> tuple[str, *tuple[str, ...]]:
    """
    Function to parse commands received from the user using the CLI.

    :param user: a string with a command and possible arguments
    :return cmd, *args: a tuple with a command in string format and
                        the arguments, if any, as a tuple of strings
    """
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

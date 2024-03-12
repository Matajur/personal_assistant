"""Module providing a functionality to manage the contacts in a contact list"""

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
)


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
            return "Provide name and phone."
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Provide contact name."
        except TypeError:
            return "Provide contact name."
        except BirthdayFormatError:
            return "Birthday must be in DD.MM.YYYY format"
        except BirthdayValidationError:
            return "Birthday cannot be in future or more than 100 years ago."
        except NameValidationError:
            return "The name must contain at least 3 characters."
        except PhoneIndexError:
            return "There is no such phone number in the record."
        except PhoneValidationError:
            return "Wrong phone number format, should be 10 digits, ex. 1234567890."
        except RecordValidationError:
            return "A contact with that name already exists."

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


def contact_adder(book: AddressBook, *_) -> str:
    """
    Function to add new records to contact book
    """
    if name_setter(book) == "0":
        return "|      |Operation cancelled                 |"
    record = name_setter(book)

    # address_setter(record)
    # phone_setter(record)
    # email_setter(record)
    # birthday_setter(record)
    # note_setter(record)

    book.add_record(record)
    return f"|Added |{record}"


@input_error
def name_setter(book: AddressBook) -> str | Record:
    """
    Function to set record name
    """
    while True:
        name = input("|      |Enter new record name ('0' to exit): ")
        if name == "0":
            return "0"
        if name in book.data.keys():
            print("|      |Record '{name}' already exists ")

        else:
            record = Record(name)
        if record:
            return record
        else:
            print("|      |Name should have from 3 up to 20 letters")


def invalid_command(*_) -> str:
    """
    Ivalid command handler.

    :return: a message about unknown command
    """
    return "|      |Invalid command                 |"


def show_contacts(book: AddressBook, *_) -> str:
    """
    Function of displaying a complete list of contacts.

    :param book: a dictionary with user contacts
    :return: a string with the full contact list or a warning that the
            contact list is empty
    """
    if len(book):
        contacts = dict(sorted(book.items()))
        result = "Contact list:"
        for _, record in contacts.items():
            result += f"\n{record}"
        return result
    return "Contact list is empty."


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

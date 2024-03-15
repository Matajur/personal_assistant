"""Module providing a console bot assistant with CLI"""

import pickle

from source.classes import AddressBook
from source.constants import COLUMN_1, SPAN, FIELD, INDENT, SEPARATOR
from source.functions import get_command, parse_input

BACKUP = "source/backup.dat"


def loader() -> AddressBook:
    """
    Function to load saved contact book.

    :return: contact book
    """
    book = AddressBook()
    try:
        with open(BACKUP, "rb") as file:
            book.data = pickle.load(file)
    except FileNotFoundError:
        pass
    return book


def main() -> None:
    """
    Function that provides Command Line Interface.
    """
    print(SEPARATOR)
    print(f"|{'Welcome to the assistant bot!':^{SPAN}}|")
    book = loader()
    if book.data:
        print(f"|{'Contact book successfully loaded':^{SPAN}}|")

    while True:
        plotter()
        print(SEPARATOR)
        user_input = input(f"|{INDENT}|Type the command: ")
        command, *args = parse_input(user_input)

        if command == "exit":
            print(SEPARATOR)
            decision = (
                input(f"|{INDENT}|Do you want to save changes? Y/N [Y]: ")
                .lower()
                .strip()
            )
            print(SEPARATOR)
            if decision in ("y", ""):
                saver(book)
                print(f"|{INDENT}|{'Changes saved, good bye!':<{FIELD}}|")
                print(SEPARATOR)
                break
            print(f"|{INDENT}|{'Good bye!':<{FIELD}}|")
            print(SEPARATOR)
            break

        get_command(command)(book, *args)


def plotter() -> None:
    """
    Main interface of the console bot
    """
    interface = {
        "1": "Show all records from contact book",
        "2": "Add new contact",
        "3": "Manage contact",
        "4": "Find contact",
        "5": "Upcoming birthdays",
        "6": "Show all records from notebook",
        "7": "Add new note",
        "8": "Manage note",
        "9": "Find note",
        "help": "Help hints",
        "exit": "Exit the bot",
    }
    print(SEPARATOR)
    for key, value in interface.items():
        print(f"|{key:^{COLUMN_1}}|{value:<{FIELD}}|")


def saver(book: AddressBook) -> None:
    """
    Function to save contact book to file.

    :param book: contact book
    """
    if book.data:
        with open(BACKUP, "wb") as file:
            pickle.dump(book.data, file)


if __name__ == "__main__":
    main()

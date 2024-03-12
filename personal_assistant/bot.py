"""Module providing a console bot assistant with CLI"""

import pickle

from source.functions import get_command, parse_input
from source.classes import AddressBook


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
    print("-" * 44)
    print("|      Welcome to the assistant bot!       |")
    book = loader()
    if book.data:
        print("|     Contact book successfully loaded     |")

    plotter()
    while True:
        user_input = input("|      |Type the command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            decision = input("Do you want to save changes? Y/N [Y]: ").lower()
            if decision in ("y", ""):
                saver(book)
                print("Changes saved, good bye!")
                break
            print("Good bye!")
            break

        print(get_command(command)(book, *args))


def plotter() -> None:
    """
    Main interface of the console bot
    """
    interface = {"1": "Show all records from contact book",
                 "2": "Add new contact",
                 "3": "Modify contact",
                 "4": "Find contact",
                 "5": "Upcoming birthdays",
                 "6": "Show all records from notebook",
                 "7": "Add new note",
                 "8": "Modify note",
                 "9": "Find note",
                 "help": "help hints",
                 "exit": "exit the bot"
                 }
    print("-" * 44)
    for key, value in interface.items():
        print(f"|{key:^6}|{value:<35}|")
    print("-" * 44)


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

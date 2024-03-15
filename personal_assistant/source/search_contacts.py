"""Module providing a functionality to search contacts in a contact list"""

import re
from typing import Callable, Any

from source.classes import (Record, AddressBook)
from source.constants import COLUMN_1, SEPARATOR, FIELD, INDENT, HEADER


def search_contacts_handler(book: AddressBook, *_) -> None:
    if not len(book):
        print(SEPARATOR)
        print(f"|{' ' * COLUMN_1}|{'Contact book is empty':<{FIELD}}|")
        return

    fn = get_search_method()
    if not fn:
        return

    contacts = dict(sorted(book.items()))
    result = fn(contacts)
    handle_search_result(result)


def get_search_method() -> Callable[[Any], Any]:
    print(SEPARATOR)
    print(f"|{'1':^{COLUMN_1}}|{'Find contact by name':<{FIELD}}|")
    print(f"|{'2':^{COLUMN_1}}|{'Find contact by phone':<{FIELD}}|")
    print(f"|{'3':^{COLUMN_1}}|{'Find contact by birthday':<{FIELD}}|")
    print(f"|{'4':^{COLUMN_1}}|{'Find contact by e-mail':<{FIELD}}|")
    print(f"|{'5':^{COLUMN_1}}|{'Find contact by address':<{FIELD}}|")
    print(f"|{INDENT}|{'Other to exit':<{FIELD}}|")
    print(SEPARATOR)
    command = input(f"|{INDENT}|{'Type the command'}: ")
    commands = {
        "1": search_contacts_by_name,
        "2": search_contacts_by_phone,
        "3": search_contacts_by_birthday,
        "4": search_contacts_by_email,
        "5": search_contacts_by_address,
    }
    return commands.get(command)


def search_contacts_by_name(contacts: Record) -> []:
    while True:
        print(SEPARATOR)
        input_value = input(f"|{INDENT}|{'Enter name'}: ")
        if 2 < len(input_value) < 21:
            result = []
            for number, record in enumerate(contacts.values()):
                search_by_name = record.search_by_name(input_value)
                if search_by_name:
                    result.append(search_by_name)
            return result

        print(SEPARATOR)
        print(f"|{INDENT}|{'The name must contain 3-20 characters':<{FIELD}}|")


def search_contacts_by_phone(contacts: Record) -> []:
    while True:
        print(SEPARATOR)
        input_value = input(f"|{INDENT}|{'Enter phone (ex. +380991234567)'}: ")
        if re.match(r"\+\d{12}", input_value):
            result = []
            for number, record in enumerate(contacts.values()):
                search_by_phone = record.search_by_phone(input_value)
                if search_by_phone:
                    result.append(search_by_phone)
            return result

        print(SEPARATOR)
        print(f"|{INDENT}|{'The phone number must have +380991234567 format':<{FIELD}}|")


def search_contacts_by_birthday(contacts: Record) -> []:
    while True:
        print(SEPARATOR)
        input_value = input(f"|{INDENT}|{'Enter birthday (ex. DD.MM.YYYY)'}: ")
        if re.match(r'^(0[1-9]|[1-2][0-9]|3[0-1])\.(0[1-9]|1[0-2])\.\d{4}$', input_value):
            result = []
            for number, record in enumerate(contacts.values()):
                search_by_birthday = record.search_by_birthday(input_value)
                if search_by_birthday:
                    result.append(search_by_birthday)
            return result

        print(SEPARATOR)
        print(f"|{INDENT}|{'Birthday must be in DD.MM.YYYY format':<{FIELD}}|")


def search_contacts_by_email(contacts: Record) -> []:
    while True:
        print(SEPARATOR)
        input_value = input(f"|{INDENT}|{'Enter email (ex. example@mail.com)'}: ")
        if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', input_value):
            result = []
            for number, record in enumerate(contacts.values()):
                search_by_email = record.search_by_email(input_value)
                if search_by_email:
                    result.append(search_by_email)
            return result

        print(SEPARATOR)
        print(f"|{INDENT}|{'The email must be in example@mail.com format':<{FIELD}}|")


def search_contacts_by_address(contacts: Record) -> []:
    while True:
        print(SEPARATOR)
        input_value = input(f"|{INDENT}|{'Enter address or press Enter to skip'}: ")
        if 2 < len(input_value) < 41:
            result = []
            for number, record in enumerate(contacts.values()):
                search_by_address = record.search_by_address(input_value)
                if search_by_address:
                    result.append(search_by_address)
            return result

        print(SEPARATOR)
        print(f"|{INDENT}|{'The address must contain 3-40 characters':<{FIELD}}|")


def handle_search_result(result: []) -> None:
    if len(result):
        print(SEPARATOR)
        print(HEADER)
        print(SEPARATOR)
        for number, record in enumerate(result):
            print(f"|{number + 1:^{COLUMN_1}}|{record}|")
    else:
        print(SEPARATOR)
        print(f"|{' ' * COLUMN_1}|{'Empty result':<{FIELD}}|")

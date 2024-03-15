"""Module providing the classes to manage the contacts in a contact book"""

import re
from collections import UserDict
from datetime import datetime

COLUMN_1 = 6
COLUMN_2 = 20
COLUMN_3 = 25
COLUMN_4 = 35
COLUMN_5 = 12
COLUMN_6 = 40
SPAN = COLUMN_1 + COLUMN_2 + COLUMN_3 + COLUMN_4 + COLUMN_5 + COLUMN_6 + 5


class BirthdayFormatError(Exception):
    """
    Incorrect birthday format error.
    """


class BirthdayValidationError(Exception):
    """
    Incorrect birthday date error.
    """


class NameValidationError(Exception):
    """
    Incorrect name format error.
    """


class PhoneIndexError(Exception):
    """
    Incorrect phone index error.
    """


class PhoneValidationError(Exception):
    """
    Incorrect phone number format error.
    """


class RecordValidationError(Exception):
    """
    Error of creating an entry with an existing name in the contact book.
    """


class Field:
    """
    A base class for record fields.
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Address(Field):
    """
    A class for storing an address.
    """


class Birthday(Field):
    """
    A class for storing a birthday. Has format validation (DD.MM.YYYY).
    """

    @property
    def value(self):
        """
        A method that validates name.
        """
        return self._value

    @value.setter
    def value(self, birthday):
        """
        A method that validates name.
        """
        try:
            birth = datetime.strptime(birthday, "%d.%m.%Y").date()
        except ValueError as exc:
            raise BirthdayFormatError() from exc
        if not 0 < (datetime.today().date() - birth).days < 100 * 365.4:
            raise BirthdayValidationError()
        self._value = datetime.strptime(birthday, "%d.%m.%Y").date()

    def __str__(self):
        return str(self.value.strftime("%d.%m.%Y"))


class Email(Field):
    """
    A class for storing a birthday. Has format validation (example@email.com).
    """

    @property
    def value(self):
        """
        A method that validates name.
        """
        return self._value

    @value.setter
    def value(self, email):
        """
        A method that validates name.
        """
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
            raise NameValidationError()
        self._value = email


class Name(Field):
    """
    A class for storing a contact name. Required field, min 3 characters.
    """

    @property
    def value(self):
        """
        A method that validates name.
        """
        return self._value

    @value.setter
    def value(self, name):
        """
        A method that validates name.
        """
        if len(str(name)) < 3:
            raise NameValidationError()
        self._value = name


class Phone(Field):
    """
    A class for storing a phone number. Has format validation (10 digits).
    """

    @property
    def value(self):
        """
        A method that validates phone number.
        """
        return self._value

    @value.setter
    def value(self, phone):
        """
        A method that validates phone number.
        """
        if not re.match(r"\+\d{12}", phone):
            raise PhoneValidationError()
        self._value = phone


class Record:
    """
    A class for storing information about a contact, including name and contacts list.
    """

    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.email = None
        self.address = None

    def add_address(self, address: str):
        """
        A method that adds an address to the record.
        """
        self.address = Address(address)

    def add_birthday(self, birthday: str):
        """
        A method that adds a birthday to the record.
        """
        self.birthday = Birthday(birthday)

    def add_email(self, email: str):
        """
        A metod that adds an email to the record.
        """
        self.email = Email(email)

    def add_phone(self, phone: str):
        """
        A method that adds a new phone number to the record.
        """
        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str):
        """
        A method that removes a phone number from the record.
        """
        index = self.find_phone(phone)
        self.phones.pop(index)

    def edit_phone(self, phones: list):
        """
        A method that edits a phone number in the record.
        """
        index = self.find_phone(phones[0])
        self.phones[index] = Phone(phones[1])

    def find_phone(self, phone: str):
        """
        A method that finds an index of the phone number in the record.
        """
        index = 0
        for item in self.phones:
            if item.value == phone:
                return index
            index += 1
        raise PhoneIndexError()

    def search_by_name(self, name: str):
        if self.name.value.lower() == name.lower():
            return self

    def search_by_phone(self, phone: str):
        for item in self.phones:
            if item.value == phone:
                return self

    def search_by_birthday(self, birthday: str):
        if str(self.birthday) == birthday:
            return self

    def search_by_email(self, email: str):
        if str(self.email).lower() == email.lower():
            return self

    def search_by_address(self, address: str):
        if str(self.address).lower() == address.lower():
            return self

    def __str__(self) -> str:
        numbers = (
            "; ".join(f"{i + 1}: {p.value}" for i, p in enumerate(self.phones))
            if self.phones
            else None
        )
        return f"{self.name.value:^{COLUMN_2}}|{str(self.email):^{COLUMN_3}}|{str(numbers):^{COLUMN_4}}|{str(self.birthday):^{COLUMN_5}}|{str(self.address):^{COLUMN_6}}"


class AddressBook(UserDict):
    """
    A class for storing and managing records.
    """

    def add_record(self, record: Record) -> None:
        """
        A method that adds a record to the address book.
        """
        if str(record.name) in self.data.keys():
            raise RecordValidationError()
        self.data[str(record.name)] = record

    def find(self, name: str) -> Record:
        """
        A method that finds a record in the address book.
        """
        return self.data[name]

    def delete(self, name: str) -> None:
        """
        A method that removes a record from the address book.
        """
        self.data.pop(name)

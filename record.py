from datetime import datetime

from constants import BIRTHDAYS_DATE_FORMAT
from errors import PhoneValidationError, BirthdayValidationError


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if self.validate(value):
            super().__init__(value)
        else:
            raise PhoneValidationError("Phone number must have 10 digits")

    @staticmethod
    def validate(phone):
        return len(phone) == 10 and phone.isdigit()


class Birthday(Field):
    def __init__(self, value):
        if self.validate(value):
            super().__init__(value)
        else:
            raise BirthdayValidationError(f"Incorrect birthday date. Correct format is {BIRTHDAYS_DATE_FORMAT}")

    @staticmethod
    def validate(date):
        return len(date) == 10 and datetime.strptime(date, BIRTHDAYS_DATE_FORMAT)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                break

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_birthday(self, date):
        self.birthday = Birthday(date)

    def __str__(self):
        birthday = f"Birthday: {self.birthday}" if self.birthday is not None else ""
        return (f"Contact name: {self.name.value}; "
                f"phones: {', '.join(p.value for p in self.phones)}; " +
                f"{birthday}"
                )

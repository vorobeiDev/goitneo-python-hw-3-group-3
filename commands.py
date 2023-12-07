from datetime import datetime, date
from collections import defaultdict

from address_book import AddressBook
from constants import WEEKDAYS, BIRTHDAYS_DATE_FORMAT
from error_handler import error_handler
from errors import ContactNotFoundError, IncorrectArgumentsQuantityError, ContactsAreEmptyError
from record import Record


@error_handler
def add_contact(args, book: AddressBook):
    if len(args) != 2:
        raise IncorrectArgumentsQuantityError("To add a new contact use 'add <name> <phone>' command.")
    name, phone = args
    contact = book.find(name=name)
    if contact is not None:
        contact.add_phone(phone=phone)
        return f"New phone was added to {name}."
    new_contact = Record(name=name)
    new_contact.add_phone(phone=phone)
    book.add_record(record=new_contact)
    return "Contact added."


@error_handler
def change_contact(args, book: AddressBook):
    if len(args) != 3:
        raise IncorrectArgumentsQuantityError("Use 'change <name> <old_phone> <phone>' command for changing contact.")
    name, old_phone, phone = args
    contact = book.find(name=name)
    if contact is None:
        raise ContactNotFoundError
    contact.edit_phone(old_phone=old_phone, new_phone=phone)
    return "Contact changed."


@error_handler
def get_phone(args, book: AddressBook):
    if len(args) != 1:
        raise IncorrectArgumentsQuantityError("To get the user's phone number please use 'phone <name>' command.")
    name = args[0]
    contact = book.find(name=name)
    if contact is None:
        raise ContactNotFoundError
    phones = contact.phones
    plural_text = "phone" if len(phones) == 1 else "phones"
    return f"{name}'s {plural_text}: {', '.join(p.value for p in phones)}"


@error_handler
def get_all_contacts(book: AddressBook):
    records = book.find_all()
    if len(records) == 0:
        raise ContactsAreEmptyError
    return "\n".join([str(record) for _, record in records])


@error_handler
def add_birthday(args, book: AddressBook):
    if len(args) != 2:
        raise IncorrectArgumentsQuantityError("To add a birthday use 'add-birthday <name> <birthday_date>' command in "
                                              f"format '{BIRTHDAYS_DATE_FORMAT}'.")
    name, birthday = args
    contact = book.find(name=name)
    if contact is None:
        raise ContactNotFoundError
    contact.add_birthday(date=birthday)
    return "Birthday added."


@error_handler
def show_birthday(args, book: AddressBook):
    if len(args) != 1:
        raise IncorrectArgumentsQuantityError("To show a birthday use 'show-birthday <name> command'.")
    name = args[0]
    contact = book.find(name=name)
    if contact is None:
        raise ContactNotFoundError
    return f"{name} was born in {contact.birthday}"


@error_handler
def get_birthdays_per_week(book: AddressBook):
    today = date.today()
    birthdays = defaultdict(list)
    records = book.find_all()

    for name, user in records:
        birthday_str = str(user.birthday)
        birthday = datetime.strptime(birthday_str, BIRTHDAYS_DATE_FORMAT).date()
        birthday_this_year = birthday.replace(year=today.year)

        if birthday_this_year < today:
            birthday_this_year = birthday_this_year.replace(year=today.year + 1)

        delta_days = (birthday_this_year - today).days

        if delta_days < 7:
            weekday = birthday_this_year.weekday()
            if weekday in [5, 6]:
                weekday = 0

            weekday_name = WEEKDAYS[weekday]
            birthdays[weekday_name].append(name)

    if len(birthdays) == 0:
        return "No birthdays"

    for day in WEEKDAYS:
        if birthdays[day]:
            return f"{day}: {', '.join((birthdays[day]))}"

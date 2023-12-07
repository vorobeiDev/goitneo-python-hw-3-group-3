from file_service import write_contacts_to_file, read_contacts_from_file
from helpers import parse_input
from commands import add_contact, change_contact, get_phone, get_all_contacts, add_birthday, show_birthday, \
    get_birthdays_per_week
from address_book import AddressBook


def main():
    book = AddressBook()
    book_from_file = read_contacts_from_file("book.pkl")
    if book_from_file is not None:
        book = book_from_file
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(get_phone(args, book))
        elif command == "all":
            print(get_all_contacts(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(get_birthdays_per_week(book))
        else:
            print("Invalid command.")

        write_contacts_to_file("book.pkl", book)


if __name__ == "__main__":
    main()

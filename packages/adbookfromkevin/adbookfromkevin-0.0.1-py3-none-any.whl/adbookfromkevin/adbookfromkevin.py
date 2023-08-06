import pandas as pd
pd.options.mode.chained_assignment = None


class Contact:
    def __init__(self, first_name, last_name, phone, email, location):
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email
        self.location = location

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def edit_first_name(self, new_first_name):
        self.first_name = new_first_name

    def edit_last_name(self, new_last_name):
        self.last_name = new_last_name

    def edit_phone(self, new_phone):
        self.phone = new_phone

    def edit_email(self, new_email):
        self.email = new_email

    def edit_location(self, new_location):
        self.location = new_location

    def __repr__(self):
        return "Name: " + self.first_name + ' ' + self.last_name + " Phone: " + \
            str(self.phone) + " Email: " + self.email + \
            " Location: " + self.location

    def __eq__(self, other):
        return isinstance(
            other,
            Contact) and (
            self.first_name,
            self.last_name,
            self.phone,
            self.email,
            self.location) == (
            other.first_name,
            other.last_name,
            other.phone,
            other.email,
            other.location)

    def __hash__(self):
        return hash(
            (self.first_name,
             self.last_name,
             self.phone,
             self.email,
             self.location))


contacts = []
favorites = []
df = pd.DataFrame(
    columns=[
        'First Name',
        'Last Name',
        'Phone',
        'Email',
        'Location'])


def create_df():
    df = pd.DataFrame(
        columns=[
            'First Name',
            'Last Name',
            'Phone',
            'Email',
            'Location'])
    return


def create_contacts():
    contacts = []
    return


def create_favorites():
    favorites = []
    return


def add_df(df):
    df.loc[len(df)] = [contacts[len(contacts) - 1].first_name,
                       contacts[len(contacts) - 1].last_name,
                       contacts[len(contacts) - 1].phone,
                       contacts[len(contacts) - 1].email,
                       contacts[len(contacts) - 1].location]
    return


def return_df():
    return df


def return_favorites():
    return favorites


def return_contacts():
    return contacts


def enter_contact():
    print("Enter your contact's information")
    first_name = input("First name: ")
    last_name = input("Last name: ")
    phone = input("Phone (10 digits): ")

    boo = True
    while boo:
        if len(phone) == 10:
            try:
                phone = int(phone)
                boo = False
            except ValueError:
                print(
                    'Please only enter numbers for phone, alphabet or others are not accepted:')
                phone = input('')
        else:
            print('Incorrect length. Please enter 10 digit:')
            phone = input('')

    email = input("Email: ")
    boo = True
    while boo:
        if "@" in email and ".com" in email:
            boo = False
        else:
            print('Email format incorrect. Please make sure @ and .com is included:')
            email = input('')

    location = input("Location (abbreviation of the state located): ")

    boo = True
    while boo:
        if location.isdigit() == False:
            if len(location) == 2:
                location = location.upper()
                boo = False
            else:
                print('Format Incorrect. Please make it is only two alphabets:')
                location = input('')
        else:
            print('Format Incorrect. Only alphabets accepted:')
            location = input('')

    our_contact = Contact(first_name, last_name, phone, email, location)
    contacts.append(our_contact)

    add_df(df)
    print("Contacts Created")
    return


def display_contact():
    print("------------Address Book Display Mode-------------------")
    if len(contacts) == 0:
        print('There is no existing contact in the address book')
        return
    else:
        for contact in contacts:
            print(contact)
        print('Contact Displayed')
    return


def display_favorite():
    print("------------Address Book Display Mode-------------------")
    if len(favorites) == 0:
        print('There is no existing favorite contact in the address book')
        return
    else:
        for fav in favorites:
            print(fav)
        print('Favorite Contact Displayed')
    return


def lookup_contact():
    to_lookup = input("Enter contact's first or last name to lookup:\n")
    exist = False
    for contact in contacts:
        if to_lookup in contact.full_name():
            print(contact)
            exist = True
    if not exist:
        print('No person found. Please try again')
    return


def filter_contact():
    print("Which filter method do you prefer?")
    print("------------Please Choose Options Below-------------------")
    print("1: Email")
    print("2: Location")
    to_lookup = int(input("Enter the number respectively:"))

    if to_lookup == 1:
        to_search = input("Which email provider? Ex: gmail ")

        temp = []
        for i in range(len(df)):
            if to_search in df['Email'][i]:
                temp.append(i)
                exist = True
                boo = False
        if not exist:
            print('No results found based on the entry')
            return

        print(df.iloc[temp])

    elif to_lookup == 2:
        to_search = input("Which Location? Ex: NY ")
        to_search = to_search.upper()
        boo = True
        while boo:

            temp = []
            if len(to_search) != 2 or to_search.isdigit():
                to_search = input('Invalid Entry. Please try again:')
                to_search = to_search.upper()
            else:
                exist = False
                for i in range(len(df)):
                    if to_search in df['Location'][i]:
                        temp.append(i)
                        exist = True
                        boo = False

                if not exist:
                    print('No results found based on the entry')
                    return

                print(df.iloc[temp])

    return df.iloc[temp]


def print_statement():
    print("Which element do you want to edit?")
    print("------------Please Choose Options Below-------------------")
    print("1: First Name")
    print("2: Last Name")
    print("3: Phone")
    print("4: Email")
    print("5: Location")
    return


def edit_info():
    to_lookup = input("Enter contact's first or last name to lookup:\n")
    exist = False
    index = []
    for id, contact in enumerate(contacts):
        if to_lookup in contact.full_name():
            print(id, contact)
            exist = True
            index.append(id)
    if not exist:
        print('There is no such person. Please try again')
        return

    to_edit = int(
        input("Which one do you want to change? Enter the respective ID:"))

    if to_edit in index:
        pass
    else:
        print('Invalid Entry. Please try again.')
        return

    print_statement()
    users_input = int(input("Select option: "))

    booo = True
    while booo:

        if users_input == 1:
            new_first_name = input('What would be the new first name?')
            contacts[to_edit].edit_first_name(new_first_name)
            return_df()['First Name'][to_edit] = new_first_name
        elif users_input == 2:
            new_last_name = input('What would be the new last name?')
            contacts[to_edit].edit_last_name(new_last_name)
            return_df()['Last Name'][to_edit] = new_last_name
        elif users_input == 3:
            new_phone = int(input("What would be the new phone number?"))
            contacts[to_edit].edit_phone(new_phone)
            return_df()['Phone'][to_edit] = new_phone
        elif users_input == 4:
            new_email = input("What would be the new email?")

            boo = True
            while boo:
                if "@" in new_email and ".com" in new_email:
                    boo = False
                else:
                    new_email = input(
                        'Email format incorrect. Please make sure @ and .com is included:')

            contacts[to_edit].edit_email(new_email)
            return_df()['Email'][to_edit] = new_email
        elif users_input == 5:
            new_location = (input("What would be the new location?")).upper()
            contacts[to_edit].edit_location(new_location)
            return_df()['Location'][to_edit] = new_location

        print("------------Changes have been saved. Please see the latest update as below:-------------------")
        print(contacts[to_edit])

        question = input(
            'Do you want to change anything else with this contact? Enter y or n:')
        if question == 'n':
            boo = False
            return

        else:
            print_statement()
            users_input = int(input("Select option: "))

    return


def delete_contact():
    to_lookup = input("Enter contact's first or last name to lookup:\n")
    exist = False
    index = []
    for id, contact in enumerate(contacts):
        if to_lookup in contact.full_name():
            print(id, contact)
            index.append(id)
            exist = True
    if not exist:
        print('There is no such person. Please try again')
        return

    to_edit = int(
        input("Which one do you want to delete? Enter the respective ID:"))
    if to_edit in index:
        contacts.pop(to_edit)
    else:
        print('Invalid Entry. Please try again.')
        return
    print("------------Changes have been saved. Please see the latest update as below:-------------------")
    for contact in contacts:
        print(contact)
    return


def add_favorite():
    to_lookup = input("Enter contact's first or last name to lookup:\n")
    exist = False
    index = []
    for id, contact in enumerate(contacts):
        if to_lookup in contact.full_name():
            print(id, contact)
            index.append(id)
            exist = True
    if not exist:
        print('There is no such person. Please try again')
        return

    to_edit = int(
        input("Which one do you want to add to favorite? Enter the respective ID:"))
    if to_edit in index:
        favorites.append(contacts[to_edit])
    else:
        print('Invalid Entry. Please try again.')
        return

    print("------------Changes have been saved. Please see the latest favorites list:-------------------")
    for fav in favorites:
        print(fav)
    print(str(len(favorites)) + ' results found')
    return


def export_csv():
    df.to_csv('contacts.csv', index=False)
    print('Successfully exported all contacts!')
    return


def terminate():
    print('Thank you. Goodbye!')
    return


main_dispatch_dict = {
    1: enter_contact,
    2: display_contact,
    3: display_favorite,
    4: filter_contact,
    5: lookup_contact,
    6: edit_info,
    7: delete_contact,
    8: add_favorite,
    9: export_csv,
    0: terminate
}


def Address_Book():
    users_input = ''
    while users_input != 0:
        try:
            print("------------Please Choose Options Below-------------------")
            print("1: Add Contact")
            print("2: Display All Contacts")
            print("3: Display Favorites")
            print("4: Filter Contact by Location and Email")
            print("5: Find Contact by Name")
            print("6: Edit Contact Information")
            print("7: Delete Contact")
            print("8: Add to Favorites")
            print("9: Export Address Book as CSV file")
            print("0: Terminate Program")
            users_input = int(input("Select option: "))
            main_dispatch_dict[users_input]()

        except ValueError:
            print('Characters selection not supported. Please try again: ')
            users_input = int(input(''))

        except KeyError:
            print('Invalid option. Please try again: ')
            users_input = int(input(''))

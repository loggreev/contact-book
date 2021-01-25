# this program lets a user perform various actions on a contact book database
# table name is contacts
# columns are first_name, last_name, phone_number, email

import sqlite3 # database
import create_database as create # create a sample database if it doesn't exist yet
import utils # useful utility functions
import os.path # file paths

def main():
    # if database doesn't exist yet, ask user if they want an empty or sample one
    if not os.path.exists(create.db_file_name):
        create.create_database()
    menuloop = True
    while menuloop:
        menuloop = menu()

# displays a menu for a user to select an option
# returns loop status
def menu():
    options = {
        'Create a new contact': create_contact,
        'Find a contact': find_contact,
        'Update a contact': update_contact,
        'Delete a contact': delete_contact,
        'Exit program': exit_program
    }
    print('What would you like to do?')
    choice = utils.get_choice(options)
    choice()
    
# create
def create_contact():
    pass
# read
def find_contact():
    pass
# update
def update_contact():
    pass
# delete
def delete_contact():
    pass
def exit_program():
    pass

if __name__ == '__main__':
    main()
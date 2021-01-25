# this program lets a user perform various actions on a contact book database
# table name is contacts
# columns are first_name, last_name, phone_number, email

import sqlite3 # database
import create_database as create # create a sample database if it doesn't exist yet
import utils # useful utility functions
import sys # exiting program
import os.path # file paths
import re # pattern searching

def main():
    # if database doesn't exist yet, ask user if they want an empty or sample one
    if not os.path.exists(create.db_file_name):
        create.create_database()
    
    # connect to database
    conn = sqlite3.connect(create.db_file_name)
    c = conn.cursor()
        
    while True:
        menu(conn, c)

# displays a menu for a user to select an option
def menu(conn, c):
    options = {
        'Create a new contact': create_contact,
        'Find a contact': find_contact,
        'Update a contact': update_contact,
        'Delete a contact': delete_contact,
        'Exit program': exit_program
    }
    print('What would you like to do?')
    choice = utils.get_choice(options)
    choice(conn, c)
    
    # save changes to database
    conn.commit()
    
# create
def create_contact(conn, c):
    phone_number = input('Contact\'s phone number (###-###-####): ')
    # phone number must be of the form ###-###-####
    if not re.search(r'^\d{3}-\d{3}-\d{4}$', phone_number):
        print('Invalid phone number.')
        return
    first_name = input('Contact\'s first name: ')
    last_name = input('Contact\'s last name: ')
    email = input('Contact\'s email address: ')
    
    values = (first_name, last_name, phone_number, email)
    
    try:
        c.execute('insert into contacts values (?,?,?,?)', values)
    except sqlite3.IntegrityError:
        print('Error: Phone number already exists.')
        return
    else:
        print('Contact added!')
    

# read
def find_contact(conn, c):
    pass

# update
def update_contact(conn, c):
    pass

# delete
def delete_contact(conn, c):
    pass

def exit_program(conn, c):
    conn.close()
    sys.exit()

if __name__ == '__main__':
    main()
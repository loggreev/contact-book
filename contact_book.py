# this program lets a user interact with a contact book database
# table name is contacts
# columns are phone_number, first_name, last_name, email

import create_database as create # create a sample database if it doesn't exist yet
import utils # useful utility functions

import sqlite3 # database
import sys # exiting program
import os.path # file paths
import re # pattern searching

def main():
    # if database doesn't exist yet, ask user if they want an empty or sample one
    if not os.path.exists(create.db_file_name):
        create.create_database()

    # object for interacting with database
    sql = sqlite_connection()
        
    while True:
        menu(sql)

# displays a menu for a user to select an option
def menu(sql):
    # run a function based on what user selects
    options = {
        'Create a new contact': create_contact,
        'Search for contacts': read_contacts,
        'Update a contact': update_contact,
        'Delete a contact': delete_contact,
        'Print search results': print_contacts,
        'Exit program': exit_program
    }
    choice = utils.get_choice(options, '\nWhat would you like to do?')
    choice(sql)
    
    # save changes to database
    sql.conn.commit()
    
# create new row in database
def create_contact(sql):
    values = get_new_row()
    if values is None:
        return
    
    try:
        sql.c.execute('insert into contacts values (?,?,?,?)', values)
    # phone number is a primary key
    except sqlite3.IntegrityError:
        print('Error: Phone number already exists.')
        return
    else:
        print('Contact added!')
    
# read certain data from the database and display it
def read_contacts(sql):
    # options that can be searched for
    options = ['Phone Number', 'First Name', 'Last Name', 'Email']
    choices = utils.get_choices(options, 'Which options do you want to search for?')
    
    # for each selected option ask user to provide a search term
    if choices:
        print('Put a % before or after your search term if you want to find the term within the data.')
    search_for = []
    for choice in choices:
        if choice == 'Phone Number':
            i = input('Phone number to search for: ')
            search_for.append(('phone_number', i))
        elif choice == 'First Name':
            i = input('First name to search for: ')
            search_for.append(('first_name', i))
        elif choice == 'Last Name':
            i = input('Last name to search for: ')
            search_for.append(('last_name', i))
        elif choice == 'Email':
            i = input('Email to search for: ')
            search_for.append(('email', i))
            
    search_for_data = tuple([data[1] for data in search_for])
    
    # construct query statement to execute
    query = 'select * from contacts'
    if search_for:
        query += ' where '
    for i, data in enumerate(search_for):
        # question marks are placeholders
        query += f'{data[0]} like ?'
        # if more things to search for
        if i+1 != len(search_for):
            query += ' and '
    
    sql.get_search_results(query, search_for_data)
    print_contacts(sql)
    
# updates an existing row
def update_contact(sql):
    if not sql.search_results:
        print('You must search for a contact before you can update it.')
        return
    
    choice = utils.get_choice(sql.search_results, 'Choose a contact to update:')
    print('Updating this contact:')
    print_contacts(sql, (choice,))
    
    values = get_new_row()
    if values is None:
        return
    values += choice
    query =  'update contacts set phone_number=?, first_name=?, last_name=?, email=? '
    query += 'where phone_number=? and first_name=? and last_name=? and email=?'
    
    try:
        sql.c.execute(query, values)
    # phone number is a primary key
    except sqlite3.IntegrityError:
        print('Error: Phone number already exists.')
        return
    else:
        print('Contact updated!')
        sql.search_results = None

# deletes an existing row
def delete_contact(sql):
    if not sql.search_results:
        print('You must search for a contact before you can delete it.')
        return
    
    choice = utils.get_choice(sql.search_results, 'Choose a contact to delete:')
    
    decision = input(f'Are you sure you want to delete this contact? (y/n)\n{choice}\n')
    if decision != 'y':
        print('Operation aborted.')
        return
    
    query = 'delete from contacts where phone_number=? and first_name=? and last_name=? and email=?'
    sql.c.execute(query, choice)
    print('Contact deleted!')
    sql.search_results = None

def exit_program(sql):
    sql.conn.close()
    sys.exit()
    
# gets data from the user for a new table row and returns it
def get_new_row():
    phone_number = input('Contact\'s phone number (###-###-####): ')
    # phone number must be of the form ###-###-####
    if not re.search(r'^\d{3}-\d{3}-\d{4}$', phone_number):
        print('Invalid phone number.')
        return None
    first_name = input('Contact\'s first name: ')
    last_name = input('Contact\'s last name: ')
    email = input('Contact\'s email address: ')
    
    return (phone_number, first_name, last_name, email)

# pretty print the provided contacts
def print_contacts(sql, contacts = None):
    if contacts is None:
        if not sql.search_results:
            print('You must search for some contacts first.')
            return
        contacts = sql.search_results
    for result in contacts:
        print(f'Phone #: {result[0]} | Name: {result[1] + " " + result[2]} | Email: {result[3]}')
    
# class for handling sqlite3 database interaction
class sqlite_connection:
    def __init__(self):
        # connect to database
        self.conn = sqlite3.connect(create.db_file_name)
        # used for queries
        self.c = self.conn.cursor()
        # results of last search
        self.search_results = None
        
    def get_search_results(self, query, data):
        # run self query to fetch results
        self.c.execute(query, data)
        self.search_results = self.c.fetchall()

if __name__ == '__main__':
    main()
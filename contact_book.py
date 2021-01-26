# this program lets a user perform various actions on a contact book database
# table name is contacts
# columns are phone_number, first_name, last_name, email

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
        
    sql = sqlite_connection()
        
    while True:
        menu(sql)

# displays a menu for a user to select an option
def menu(sql):
    options = {
        'Create a new contact': create_contact,
        'Find a contact': find_contact,
        'Update a contact': update_contact,
        'Delete a contact': delete_contact,
        'Exit program': exit_program
    }
    # run a function based on what user selects
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
def find_contact(sql):
    # options that can be searched for
    options = ['Phone Number', 'First Name', 'Last Name', 'Email']
    choices = utils.get_choices(options, 'Which options do you want to search for?')
    
    # for each selected option ask user to provide a search term
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
    
# update
def update_contact(sql):
    if not sql.search_results:
        print('You must search for a contact before you can update it.')
        return
    
    choice = utils.get_choice(sql.search_results, 'Choose a contact to update:')
    
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

# delete
def delete_contact(sql):
    pass

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
        print()
        for result in self.search_results:
            # print(f'Phone #: {result[0]}\nName: {result[1] + " " + result[2]}\nEmail: {result[3]}\n')
            print(result)
        

if __name__ == '__main__':
    main()
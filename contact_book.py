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
    choice = utils.get_choice(options, '\nWhat would you like to do?')
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
    
    values = (phone_number, first_name, last_name, email)
    
    try:
        c.execute('insert into contacts values (?,?,?,?)', values)
    except sqlite3.IntegrityError:
        print('Error: Phone number already exists.')
        return
    else:
        print('Contact added!')
    

# read
def find_contact(conn, c):
    options = ['Phone Number', 'First Name', 'Last Name', 'Email']
    choices = utils.get_choices(options, 'Which options do you want to search for?')
    
    print('Put a % before or after your term if you want to find the term within the data.')
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
    
    # construct sql statement to execute
    sql = 'select * from contacts'
    if search_for:
        sql += ' where '
    for i, data in enumerate(search_for):
        sql += f'{data[0]} like ?'
        # more things to search for
        if i+1 != len(search_for):
            sql += ' and '
    
    # print(sql)
    # print(search_for_data)
    c.execute(sql, search_for_data)
    results = c.fetchall()
    for result in results:
        print(f'Phone #: {result[0]}\nName: {result[1] + " " + result[2]}\nEmail: {result[3]}\n')
    

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
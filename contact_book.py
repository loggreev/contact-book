# this program lets a user perform various actions on a contact book database
# table name is contacts
# columns are first_name, last_name, phone_number, email

import sqlite3 # database
import create_database as create # create a sample database if it doesn't exist yet
import os.path # file paths

def main():
    # if database doesn't exist yet, ask user if they want an empty or sample one
    if not os.path.exists(create.db_file_name):
        create.create_database()

# create
# read
# update
# delete

if __name__ == '__main__':
    main()
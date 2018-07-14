import functools
import hashlib
import os
import sqlite3
import sys

from cli import *
from files.management import *

conn = None
c = None
db_file = ''


def is_db_configured():
    if not c and not conn:
        print('[!] Database file not specified')
        return False
    return True


def select_db(db_file_name):
    global conn
    global c
    global db_file

    db_file = db_file_name

    if db_file not in list_db_files():
        print(f'[i] Creating database {db_file}')

    conn = sqlite3.connect(db_file_name)
    c = conn.cursor()
    print(f'[i] Selected database is {db_file}')


def current_db():
    if is_db_configured():
        print(f'[i] Current database is {db_file}')


def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS passwords (hash TEXT, password TEXT UNIQUE)')


def add_to_db(file_name, fast=False, encoding='latin-1'):
    """
    This function reads passwords from file and
    adds them as well as their hashed equivalents
    to database.
    """
    if not os.path.isfile(file_name):
        print('[!] File does not exists')
        return
    if is_db_configured():
        create_table()

        with open(file_name, 'r', encoding=encoding) as f:
            parts = 1

            if fast:
                c.execute('PRAGMA synchronous=OFF')

            print('[i] Splitting data into parts')
            for chunk in read_in_chunks(f):
                c.execute('BEGIN TRANSACTION ')

                for password in chunk:
                    hashed_password = hashlib.md5()
                    hashed_password.update(bytes(password, encoding))

                    c.execute('INSERT OR IGNORE INTO passwords VALUES (?, ?)', (hashed_password.hexdigest(), password))

                c.execute('COMMIT')
                print(f'[+] Part {parts} completed')
                parts += 1
            print(f'[+] Successfully added {file_name} to database')


def search_in_db(hashed_password):
    if is_db_configured():
        print('[i] Started looking for password')
        c.execute('SELECT * FROM passwords WHERE hash=?', (hashed_password,))
        row = c.fetchone()

        if row:
            print(f'[+] Password found: {row[1]}')
        else:
            print('[!] Password not found')


def algorithms_supported():
    print(hashlib.algorithms_available)


def cracken_exit():
    if is_db_configured():
        c.close()
        conn.close()
    sys.exit()


def main():
    menu()

    single_options = {
        'select_db': select_db,
        'add': functools.partial(add_to_db, fast=False),
        'fast_add': functools.partial(add_to_db, fast=True),
        'crack': search_in_db,
    }

    args_options = {

        'list_db': list_db_files,
        'current_db': current_db,
        'algorithms_supported': algorithms_supported,
        'menu': menu,
        'help': hints,
        'exit': cracken_exit,
    }

    while True:
        command = input('\n> ')
        command = command.split(' ')

        if len(command) == 2 and command[0] in single_options:
            single_options[command[0]](command[1])
        elif len(command) == 1 and command[0] in args_options:
            args_options[command[0]]()
        else:
            print('Invalid command')


if __name__ == '__main__':
    main()


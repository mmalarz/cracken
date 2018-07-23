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


SUPPORTED_ALGORITHMS = {
    'md5': hashlib.md5,
    'sha256': hashlib.sha256,
    'sha384': hashlib.sha384,
    'sha512': hashlib.sha512
}


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


def supported_algorithms():
    for alg in SUPPORTED_ALGORITHMS:
        print(alg)


def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS passwords (hash TEXT, password TEXT UNIQUE)')


def get_algorithm():
    supported_algorithms()
    while True:
        algorithm = str(input('Algorithm to use while hashing password: ')).lower()
        if algorithm in SUPPORTED_ALGORITHMS:
            return algorithm
        else:
            print('Algorithm not supported')


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
        algorithm = get_algorithm()
        create_table()

        with open(file_name, 'r', encoding=encoding) as f:
            parts = 1

            if fast:
                c.execute('PRAGMA synchronous=OFF')

            print('[i] Splitting data into parts')
            for chunk in read_in_chunks(f):
                c.execute('BEGIN TRANSACTION ')

                for password in chunk:
                    hashed_password = SUPPORTED_ALGORITHMS[algorithm]()
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


def cracken_exit():
    if is_db_configured():
        c.close()
        conn.close()
    sys.exit()


def main():
    menu()

    single_arg_options = {
        'select_db': select_db,
        'add': functools.partial(add_to_db, fast=False),
        'fast_add': functools.partial(add_to_db, fast=True),
        'crack': search_in_db,
    }

    no_args_options = {
        'list_db': list_db_files,
        'current_db': current_db,
        'algorithms_supported': supported_algorithms,
        'menu': menu,
        'help': hints,
        'exit': cracken_exit,
    }

    while True:
        command = input('\n> ')
        command = command.split(' ')

        if len(command) == 2 and command[0] in single_arg_options:
            single_arg_options[command[0]](command[1])
        elif len(command) == 1 and command[0] in no_args_options:
            no_args_options[command[0]]()
        else:
            print('Invalid command')


if __name__ == '__main__':
    main()

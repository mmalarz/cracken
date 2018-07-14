import glob
import itertools


def list_db_files():
    db_list = [file for file in glob.glob('*.db')]
    print(db_list)
    return db_list


def read_in_chunks(file_object, chunk_size=1000000):
    """
    Lazy function (generator) that reads a file piece by piece.
    """
    while True:
        data = [line.strip() for line in itertools.islice(file_object, chunk_size)]
        if not data:
            break
        yield data

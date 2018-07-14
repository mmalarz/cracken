def menu():
    print("""
     _/_/_/  _/_/_/      _/_/      _/_/_/  _/    _/  _/_/_/_/  _/      _/   
  _/        _/    _/  _/    _/  _/        _/  _/    _/        _/_/    _/    
 _/        _/_/_/    _/_/_/_/  _/        _/_/      _/_/_/    _/  _/  _/     
_/        _/    _/  _/    _/  _/        _/  _/    _/        _/    _/_/      
 _/_/_/  _/    _/  _/    _/    _/_/_/  _/    _/  _/_/_/_/  _/      _/


    |------------------------|
    |        Commands        |
    |------------------------|
    | list_db                |
    |------------------------|
    | select_db <db_file>    |
    |------------------------|
    | current_db             |
    |------------------------|
    | add <file_path>        |
    |------------------------|
    | fast_add <file_path>   |
    |------------------------|
    | crack <hash>           |
    |------------------------|
    | algorithms_supported   |
    |------------------------|
    | menu                   |
    |------------------------|
    | help                   |
    |------------------------|
    | exit                   |
    |------------------------|""")


def hints():
    print("""list_db                 - list all created database files
select_db <db_file>     - select or create new database to work with
current_db              - prints selected database
add <file_path>         - add passwords file to database
fast_add <file_path>    - adds passwords faster, but problems can occur when process will be stopped
crack <hash>            - looks for given hash in database
algorithms_supported    - list of supported hashing algorithms
menu                    - prints cracken menu
exit                    - exits script""")


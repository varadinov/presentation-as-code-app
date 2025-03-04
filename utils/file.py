
import datetime
import os


def load_file(path: str) -> str:
    with open(path, 'r') as file:
        return file.read()
    
def get_file_creation_time(path: str) -> str:
    file_stat = os.stat(path)
    creation_time = file_stat.st_ctime  
    return datetime.datetime.fromtimestamp(creation_time)
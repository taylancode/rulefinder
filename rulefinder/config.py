#!/usr/bin/python
from configparser import ConfigParser
import os

def config(filename='database.ini', section='postgresql') -> dict:
    path = os.path.dirname(os.path.abspath(__file__))
    filepath = (f"{path}\{filename}")

    parser = ConfigParser()
    parser.read(filepath)

    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(f'Section {section} not found in the {filename} file')

    return db

#!/bin/env python3

from sys import argv

from src.website.google_search_engine import search_in_google
from datetime import datetime


def main():
    start_time = datetime.now()
    argc = len(argv)

    if argc != 3:
        print('Usage:\n\tpython main.py [FirstName] [LastName]')
        return -1
    print(search_in_google("%s %s" % (argv[1], argv[2])))
    print(datetime.now() - start_time)
    return 0


if __name__ == "__main__":
    main()

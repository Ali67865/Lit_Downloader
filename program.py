from tinydb import TinyDB, Query
import beautifulsoup4

db = TinyDB('db.json')

DBEntry = collections.namedtuple('DBEntry',
                                       'author, story, tags, address')


def print_header():
    print('--------------------------')
    print('------LIT DOWNLOADER------')
    print('--------------------------')


def parse_webpage():
    pass


def check_if_last_page():
    pass


def insert_into_DB():
    pass

def main():



if __name__ == '__main__':
    main()
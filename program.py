from tinydb import TinyDB, Query
import requests
import bs4
import collections
import re

db = TinyDB('db.json')

DBEntry = collections.namedtuple('DBEntry',
                                       'title, category, author, short_description, story, tags, address, rating')


def print_header():
    print('--------------------------')
    print('------LIT DOWNLOADER------')
    print('--------------------------')


def get_html(url):
    response = requests.get(url)
    #print(response.status_code)
    #print(response.text)

    return response.text

def get_author(html):
    soup = bs4.BeautifulSoup(html, 'html.parser')
    author = soup.find(class_='b-story-header').find(class_='b-story-user-y').find('a').get_text()
    #print(author)
    return author

def get_rating():
    pass

def get_story():
    pass

def get_tags():
    pass

def get_title(html):
    soup = bs4.BeautifulSoup(html, 'html.parser')
    title = soup.find('title').get_text().split(" - ")[0]
    #print(title)
    return title

def get_category(html):
    soup = bs4.BeautifulSoup(html, 'html.parser')
    category = soup.find('title').get_text().split(" - ")[1]
    #print(category)
    return category

def get_short_description(html):
    soup = bs4.BeautifulSoup(html, 'html.parser')
    desc = soup.findAll(attrs={"name": re.compile(r"description", re.I)})
    short_description = (desc[0]['content'])
    #print(short_description)
    return short_description


def check_if_last_page():
    pass


def insert_into_DB():
    pass

def main():
    address = 'https://www.literotica.com/s/first-time-milking'
    html = get_html(address)
    title = get_title(html)
    category = get_category(html)
    author = get_author(html)
    short_description = get_short_description(html)


if __name__ == '__main__':
    main()
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

def get_number_of_pages(html):
    soup = bs4.BeautifulSoup(html, 'html.parser')
    page_count = len(soup.findAll(attrs={"name": re.compile(r"page", re.I)})[0].contents)
    #print(page_count)
    return page_count

    #[<select name="page"><option class="current" selected="selected" value="1">1</option><option value="2">2</option></select>]

def get_author(html):
    soup = bs4.BeautifulSoup(html, 'html.parser')
    author = soup.find(class_='b-story-header').find(class_='b-story-user-y').find('a').get_text()
    #print(author)
    return author

def get_rating():
    pass

def get_story(url, page_count):
    story = ''
    for page_number in range(1, page_count+1):
        story += get_page_story(url, page_number)
    return story


def get_page_story(url: str, page_number):
    if page_number > 1:
        url = url + '?page=' + str(page_number)
    html = get_html(url)
    soup = bs4.BeautifulSoup(html, 'html.parser')
    page_story = soup.find(class_='b-story-body-x x-r15').find('p').get_text()
    return page_story

def get_tags(url):
    html = get_html(url)
    soup = bs4.BeautifulSoup(html, 'html.parser')
    ul = soup.find(class_='b-s-story-tag-list').find('ul').get_text()
    ##content > div.b-sidebar > div:nth-child(3) > div.b-box-body > div
    #<div class="b-s-story-tag-list"><ul><li><a href="https://tags.literotica.com/linds%20continued">linds continued</a>&nbsp;– </li><li><a href="https://tags.literotica.com/linds%20laughed">linds laughed</a>&nbsp;– </li><li><a href="https://tags.literotica.com/watched%20joan">watched joan</a>&nbsp;– </li><li><a href="https://tags.literotica.com/toes%20joan">toes joan</a>&nbsp;– </li><li><a href="https://tags.literotica.com/cock%20linds">cock linds</a>&nbsp;– </li><li><a href="https://tags.literotica.com/shapely%20calf">shapely calf</a>&nbsp;– </li><li><a href="https://tags.literotica.com/linds%20giggled">linds giggled</a>&nbsp;– </li><li><a href="https://tags.literotica.com/shaft%20linds">shaft linds</a>&nbsp;– </li><li><a href="https://tags.literotica.com/linds%20commented">linds commented</a>&nbsp;– </li><li><a href="https://tags.literotica.com/locked%20toes">locked toes</a></li></ul></div>
    tag_list = []
    for tag in ul.split(' – '):
        tag_list.append(tag)
    return tag_list

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
    return short_description


def insert_into_DB():
    pass

def main():
    address = 'https://www.literotica.com/s/first-time-milking'
    html = get_html(address)
    title = get_title(html)
    category = get_category(html)
    author = get_author(html)
    short_description = get_short_description(html)
    page_count = get_number_of_pages(html)
    story = get_story(address, page_count)

    if page_count > 1:
        address = address + '?page=' + str(page_count)

    tags = get_tags(address)
    rating = get_rating(address)


if __name__ == '__main__':
    main()
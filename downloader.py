from tinydb import TinyDB, Query
import requests
import bs4
import collections
import re

db = TinyDB('db.json')

DBEntry = collections.namedtuple('DBEntry', 'title, category, author, short_description, story, tags, address')


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
    try:
        page_count = len(soup.findAll(attrs={"name": re.compile(r"page", re.I)})[0].contents)
    except:
        page_count = 1
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
    tag_list = []
    try:
        ul = soup.find(class_='b-s-story-tag-list').find('ul').get_text()
        ##content > div.b-sidebar > div:nth-child(3) > div.b-box-body > div
        #<div class="b-s-story-tag-list"><ul><li><a href="https://tags.literotica.com/linds%20continued">linds continued</a>&nbsp;– </li><li><a href="https://tags.literotica.com/linds%20laughed">linds laughed</a>&nbsp;– </li><li><a href="https://tags.literotica.com/watched%20joan">watched joan</a>&nbsp;– </li><li><a href="https://tags.literotica.com/toes%20joan">toes joan</a>&nbsp;– </li><li><a href="https://tags.literotica.com/cock%20linds">cock linds</a>&nbsp;– </li><li><a href="https://tags.literotica.com/shapely%20calf">shapely calf</a>&nbsp;– </li><li><a href="https://tags.literotica.com/linds%20giggled">linds giggled</a>&nbsp;– </li><li><a href="https://tags.literotica.com/shaft%20linds">shaft linds</a>&nbsp;– </li><li><a href="https://tags.literotica.com/linds%20commented">linds commented</a>&nbsp;– </li><li><a href="https://tags.literotica.com/locked%20toes">locked toes</a></li></ul></div>
        for tag in ul.split(' – '):
            tag_list.append(tag)
    except:
        print('no tags found')
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


def insert_into_DB(obj: DBEntry):
    #'DBEntry','title, category, author, short_description, story, tags, address'
    string_tags = ''.join(obj.tags)
    query = Query()
    query_result = db.search(query.address == obj.address)
    if not query_result:
        db.insert({'title': obj.title, 'category': obj.category, 'author': obj.author, 'short_description': obj.short_description, 'story': obj.story, 'tags': obj.tags, 'address': obj.address})
    else:
        print('story already in DB!')


def story_does_not_exist(url:str):
    html = get_html(url)
    soup = bs4.BeautifulSoup(html, 'html.parser')
    error_404 = soup.findAll(text=re.compile('Error 404'))
    error_410 = soup.findAll(text=re.compile('Error 410'))
    maintenance = soup.findAll(text=re.compile('Literotica is undergoing maintenance'))

    if not error_404 and not error_410 and not maintenance:
        return False
    else:
        return True

def downloader_main(url: str):

    html = get_html(url)
    query = Query()
    query_result = db.search(query.address == url)
    doesnt_exist = story_does_not_exist(url)
    if query_result:
        print('story already in DB!')
        return 1
    elif doesnt_exist:
        print('story currently not available')
        return 2
    else:
        title = get_title(html)
        category = get_category(html)
        author = get_author(html)
        short_description = get_short_description(html)
        page_count = get_number_of_pages(html)
        story = get_story(url, page_count)

        if page_count > 1:
            last_page = url + '?page=' + str(page_count)
        else:
            last_page = url
        tags = get_tags(last_page)
        #rating = get_rating(address)
        #'DBEntry','title, category, author, short_description, story, tags, address'
        obj = DBEntry (title=title, category=category, author=author, short_description=short_description, story=story, tags=tags, address=url)
        insert_into_DB(obj)
        return 0

if __name__ == '__main__':
   downloader_main("https://www.literotica.com/s/fun-for-don-and-kathy-pt-02")

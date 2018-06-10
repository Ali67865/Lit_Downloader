import downloader
import os
import bs4

def get_absolute_filename(name):
    filename = os.path.abspath(os.path.join('.', name + '.html'))
    return filename

def parse_instapaper_html(name: str):
    link_list = []
    fullpath = get_absolute_filename(name)
    soup = bs4.BeautifulSoup(open(fullpath), 'html.parser')
    for item in soup.findAll('a', href=True):
        #print(item.get('href'))
        link_list.append(item.get('href'))
    return link_list

def filter_non_relevant_addresses(link_list):
    new_list = []
    for entry in link_list:
        entry_string = str(entry)
        #if entry_string.contains('https://www.literotica.com/s/'):
        if ('https://www.literotica.com/s/' in entry_string) or ('http://www.literotica.com/s/' in entry_string):
            new_list.append(entry)
    return new_list

def main():

    link_list = parse_instapaper_html('instapaper-export-3')
    parsed_list = filter_non_relevant_addresses(link_list)

if __name__ == '__main__':
    main()

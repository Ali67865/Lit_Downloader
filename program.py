import downloader
import os
import bs4
import random
import time


def get_absolute_filename(name):
    filename = os.path.abspath(os.path.join('.', name + '.html'))
    return filename


def parse_instapaper_html(name: str):
    link_list = []
    fullpath = get_absolute_filename(name)
    soup = bs4.BeautifulSoup(open(fullpath), 'html.parser')
    for item in soup.findAll('a', href=True):
        # print(item.get('href'))
        link_list.append(item.get('href'))
    return link_list


def filter_non_relevant_addresses(link_list):
    new_list = []
    discarded_list = []
    for entry in link_list:
        entry_string = str(entry)
        # if entry_string.contains('https://www.literotica.com/s/'):
        if ('https://www.literotica.com/s/' in entry_string) or ('http://www.literotica.com/s/' in entry_string) or (
                'https://literotica.com/s/' in entry_string) or ('https://literotica.com/stories/' in entry_string):
            new_list.append(entry)
        else:
            discarded_list.append(entry)

    return new_list


def main():
    link_list = parse_instapaper_html('instapaper-export-4')
    parsed_list = filter_non_relevant_addresses(link_list)
    total = parsed_list.__len__()
    i = 1300
    for url in parsed_list[i:]:
        print('downloading {} of {} = ({})'.format(i, total, url))
        retvalue = downloader.downloader_main(url)
        if retvalue == 0:
            r = random.randrange(10, 100)
            print('done, sleeping ({})...'.format(r))
            time_delay = r
            time.sleep(time_delay)
        else:
            print('skipped, moving on...')
        i = i+1


if __name__ == '__main__':
    main()

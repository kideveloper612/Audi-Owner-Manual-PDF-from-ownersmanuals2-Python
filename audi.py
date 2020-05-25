import requests
import os
import csv
import time
import re
from bs4 import BeautifulSoup as Be


def send_request(url, method="GET", payload={}):
    try:
        res = requests.request(url=url, method=method, data=payload)
        if res.status_code == 200:
            return res
        return send_request(url=url, method=method, payload=payload)
    except ConnectionError:
        time.sleep(10)
        return send_request(url=url, method=method, payload=payload)


def url_soup(url):
    res = send_request(url=url, method="GET", payload={})
    return Be(res.text, 'html5lib')


def write_csv(lines, file_name):
    file = open(file_name, 'a', encoding='utf-8', newline='')
    writer = csv.writer(file, delimiter=',')
    writer.writerows(lines)
    file.close()


def main():
    base_soup = url_soup(url=base_url)
    cards = base_soup.select('.nav.nav-pills.nav-stacked li a')
    for card in cards:
        card_text_soup = card.find(text=True, recursive=False).strip()
        year = card_text_soup[:4]
        model = card_text_soup.replace(year, '').replace(make, '').strip()
        link_soup = url_soup(url='https://ownersmanuals2.com' + card['href']).select('.ulb2 .nav.nav-pills.nav-stacked li a')[0]
        link = 'https://ownersmanuals2.com' + link_soup['href']
        link_soup = url_soup(url=link)
        title = link_soup.find(attrs={'class': 'manual_title'}).text.strip()
        description_soup = link_soup.find(text=re.compile('Manual Description'))
        if description_soup:
            description = description_soup.parent.next_sibling.next_sibling.text.strip()
        else:
            description = ''
        manual_url_soup = link_soup.find(attrs={'class': 'btn btn-primary'})
        if manual_url_soup:
            manual_url = 'https://ownersmanuals2.com' + manual_url_soup['href']
        line = [year, make, model, 'PDF', title, description, manual_url]
        print(line)
        write_csv(lines=[line], file_name='Audi_MANUAL.csv')


if __name__ == '__main__':
    print('----- Start -----')
    base_url = 'https://ownersmanuals2.com/make/audi'
    make = 'Audi'
    csv_header = ['YEAR', 'MAKE', 'MODEL', 'SECTION', 'TITLE', 'DESCRIPTION', 'PDF']
    write_csv(lines=[csv_header], file_name='Audi_MANUAL.csv')
    main()
    print('---- The End ----')
import requests 
import csv
from datetime import datetime
from time import sleep
from multiprocessing import Pool
from bs4 import BeautifulSoup

def get_html(url):
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
    r = requests.get(url, headers=header)
    return r.text


def get_links(html):
    soup = BeautifulSoup(html, 'lxml')
    tds = soup.find('table', class_='items').find_all('div', class_='names')
    links = []
    for td in tds:
        a = td.find('a').get('href')
        link = 'https://myfin.by' + a 
        links.append(link) 

    return links


def get_page_date(html):
    soup = BeautifulSoup(html, 'lxml')
    try:
        name = soup.find('h1').text.strip()
    except:
        name = ''

    try:
        last_update = soup.find('div', class_='birzha_info_head_avg_time').text.strip()
    except :
        last_update = ''

    try:
        weighted_average_course = soup.find('div', class_='birzha_info_head_rates').text.strip()
    except:
        weighted_average_course = ''

    try:
        change_per_day = soup.find('div', class_='up').text.strip()
    except:
        change_per_day = ''

    try:
        starting_course = soup.find('div', class_='birzha_info_head_open birzha_head_t').text.strip()
    except:
        starting_course = ''

    data = { 'name' : name,
             'last_update': last_update,
             'weighted_average_course' : weighted_average_course,
             'change_per_day' : change_per_day,
             'starting_course' : starting_course }
    return data

def write_csv(data):
    with open('cryptocurrency.csv', 'a') as file:
        writer = csv.writer(file)

        writer.writerow( ( data['name'],
                           data['last_update'],
                           data['weighted_average_course'],
                           data['change_per_day'],
                           data['starting_course'] ) )
        print (data['name'], 'parsed')

def make_all(url):
    html = get_html(url)
    data = get_page_date(html)
    write_csv(data)

def get_all_links():
    count = 1
    max_page = 3
    pages = []
    all_url = []
    url = 'https://myfin.by/crypto-rates/?page='
    for x in range(1, max_page + 1):
        pages.append(url + str(x)) 
        
    for  r in pages:
        all_links = get_links(get_html(r))
        all_url.extend(all_links)
        print('Кол-во ссылок : ' + str(len(all_links)) + ' на странице: ' + str(count))
        count = count + 1
        
    with  Pool(10) as P:
        P.map(make_all, all_url)  
    
def main():
    start = datetime.now()
    get_all_links()

    end = datetime.now()
    total = end - start
    print(str(total))


if  __name__ == "__main__":
    main()
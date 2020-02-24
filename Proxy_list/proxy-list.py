import requests 
import csv
from datetime import datetime
from time import sleep
from multiprocessing import Pool
from bs4 import BeautifulSoup
import json

def get_html(url):
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
    r = requests.get(url, headers=header)
    return r.text

def get_proxy_list(html):
    soup = BeautifulSoup(html, 'lxml')
    tbody = soup.find('tbody')
    IP_PORT = []
    ALL_LIST_PROXY = {}
    print('Начало парсинга данных !')
    try:
        for row in tbody.find_all('tr'):
            tmp = row.find_all('td')
            ALL_LIST_PROXY = { 
                'LIST_IP' : {
                                'IP-adress': tmp[0].text,
                                'PORT': tmp[1].text,
                                'Country': tmp[3].text,
                                'Anonimity' : tmp[4].text,
                                'Https' : tmp[6].text,
                                'Last Checked' : tmp[7].text,
                }
            }
            IP_PORT.append(ALL_LIST_PROXY)
        count = len(IP_PORT)
        print('Кол-во IP-адресов: ' + str(count))
    except:
        print(' Ошибка ! \n Проверти пожалуйста соединение с интернетом !')
    print('Конец парсинга данных !')
    return IP_PORT



def Write_To_Json(IP):
    print('Начало записи данных в json !')
    count = len(IP)
    with open('proxys.json','w') as jf:
        list_data = {
            'Count' : count,
            'IP' : IP
        }
        json.dump(list_data,jf,indent=4)
    print('Конец записи данных в json !')

def main():
    start = datetime.now()
    URL = 'https://free-proxy-list.net/'

    print('Парсинг IP-Адресов с сайта : ' + URL)
    HTML = get_proxy_list(get_html(URL))

    Write_To_Json(HTML)
    
    end = datetime.now()
    total = end - start
    print('Время выполнения программы : ' + str(total))

if  __name__ == "__main__":
    main()
import os
import requests
from datetime import datetime
from bs4 import BeautifulSoup


KEYWORDS = ['дизайн']
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/101.0.4951.67 Safari/537.36'
}
url = 'https://habr.com/ru/all/'


def logger(old_function):
    def new_function(*args, **kwargs):
        result = old_function(*args, **kwargs)
        with open('log.txt', "a") as f:
            f.write(f'Дата и время вызова функции: {datetime.now().strftime("%d-%m-%Y [%H:%M:%S]")}\n')
            f.write(f'Наменование функции: {old_function.__name__}\n')
            f.write(f'Аргументы: {args}, {kwargs}\n')
            f.write(f'Возвращаемое значение: {result}\n')
            f.write('*' * 60 + '\n')
        return result
    return new_function


def logger_with_path(log_path):
    def logger(old_function):
        def new_function(*args, **kwargs):
            result = old_function(*args, **kwargs)
            with open(os.path.join(log_path), "a") as f:
                f.write(f'Дата и время вызова функции: {datetime.now().strftime("%d-%m-%Y [%H:%M:%S]")}\n')
                f.write(f'Наменование функции: {old_function.__name__}\n')
                f.write(f'Аргументы: {args}, {kwargs}\n')
                f.write(f'Возвращаемое значение: {result}\n')
                f.write('*' * 60 + '\n')
            return result
        return new_function
    return logger


@logger_with_path(r'C:\Project\ADPY_Homework_5\log.txt')
def parser(url):
    page = 1

    while True:
        response = requests.get(url + 'page' + str(page), headers=HEADERS)
        soup = BeautifulSoup(response.text, 'html.parser')
        all_snippets = soup.find_all(class_='tm-article-snippet')
        if len(all_snippets):
            for snippet in all_snippets:
                for keyword in KEYWORDS:
                    if snippet.text.lower().find(keyword) > 0:
                        data = snippet.find('time').get('title')
                        header = snippet.find('h2').find('span').text
                        link = snippet.find('h2').find('a').get('href')
                        print(f'{data} - {header} - {"https://habr.com" + link}')
            page += 1
        else:
            break


parser(url)

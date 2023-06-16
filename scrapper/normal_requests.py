from math import ceil

import requests
from bs4 import BeautifulSoup
from fake_headers import Headers


def get_total_pages() -> int:
    result = requests.get('https://hh.ru/search/vacancy?area=1&area=2'
                          '&search_field=description&search_field=name&enable_snippets=false'
                          '&text=Django%2C+flask.+python&ored_clusters=true&page=0',
                          headers=Headers(headers=True).generate())

    soup = BeautifulSoup(result.content, 'html.parser')

    total_find_block_tag = soup.find(
        attrs={'data-qa': 'vacancies-search-header'})
    count_vacancies_tag = total_find_block_tag.find(
        attrs={'data-qa': 'bloko-header-3'})

    total_vacancies = int(count_vacancies_tag.text.split()[0])

    return ceil(total_vacancies / 50)
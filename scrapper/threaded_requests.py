from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from os import getcwd

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm

from .normal_requests import get_total_pages

date_template = '%H:%M:%S'


def _parse_page(page_num: int) -> tuple[int, str]:
    chrome_options = Options()
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument('--headless=new')
    driver = webdriver.Chrome(
        executable_path=f'{getcwd()}/scrapper/drivers/chromedriver',
        options=chrome_options)

    driver.get('https://hh.ru/search/vacancy'
               '?area=1&area=2&search_field=description&'
               'search_field=name&enable_snippets=false&'
               'text=Django%2C+flask.+python&ored_clusters=true&'
               f'page={page_num}')

    page_source = driver.page_source

    driver.quit()

    return page_num, page_source


def get_all_pages(max_workers: int) -> dict[int, str]:
    total_pages = get_total_pages()
    print(f'{datetime.now().strftime(date_template)} | starting parsing')

    page_sources = {}
    with tqdm(total=total_pages, colour='green',
              desc=f'{datetime.now().strftime(date_template)} | ',
              bar_format='{desc}{percentage:3.0f}%|{bar}{r_bar}'
              ) as pbar:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            for result in executor.map(_parse_page, range(0, total_pages)):
                page_sources[result[0]] = result[1]
                pbar.update(1)

    print(
        f'{datetime.now().strftime(date_template)} '
        f'| finished parsing')

    return page_sources

from bs4 import BeautifulSoup, Tag

from scrapper.threaded_requests import get_all_pages


class HHParser:
    def __init__(self, max_workers: int):
        self.raw_pages = get_all_pages(max_workers)
        self.soups = self._brew_soups()
        self.article_body_tags = self._get_article_body_tags()
        self._remove_blank_pages()
        self.vacancies_info = self.get_body_info()

    def _remove_blank_pages(self) -> None:
        pages_to_remove = []

        for page, content in self.article_body_tags.items():
            if not content:
                pages_to_remove.append(page)

        for page in pages_to_remove:
            del self.article_body_tags[page]

    def _brew_soups(self) -> dict[int, BeautifulSoup]:
        soups = {}
        for page_num, source in self.raw_pages.items():
            soups[page_num] = BeautifulSoup(source, 'html.parser')

        return soups

    def _get_article_body_tags(self) -> dict[int, list[Tag]]:
        articles = {}
        for page_num, soup in self.soups.items():
            articles[page_num] = soup.find_all(
                class_='vacancy-serp-item-body')

        return articles

    def get_body_info(self) -> list[dict[str, str]]:
        info = []
        for page in self.article_body_tags.values():
            for vacancy in page:
                title = vacancy.find(class_='serp-item__title')
                compensation = vacancy.find(
                    attrs={'data-qa': 'vacancy-serp__vacancy-compensation'}
                )
                city = vacancy.find(
                    attrs={'data-qa': 'vacancy-serp__vacancy-address'}
                )
                link = title['href']

                vacancy_info = {
                    'title': ' '.join(title.text.split()),
                    'compensation': ' '.join(
                        compensation.text.split()) if compensation else 'N/A',
                    'city': ' '.join(city.text.split()),
                    'link': link
                }

                info.append(vacancy_info)

        return info

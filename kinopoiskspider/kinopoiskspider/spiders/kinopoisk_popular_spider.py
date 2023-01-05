import os
import scrapy
from urllib.parse import urlencode
from kinopoiskspider.exceptions import MissingEnvironmentVariable

API_KEY = os.getenv('API_KEY')
if not API_KEY:
    raise MissingEnvironmentVariable('Set API_KEY env variable in Dockerfile')


def get_proxy_url(url):
    payload = {'api_key': API_KEY, 'url': url}
    proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
    return proxy_url


class KinopoiskPopularSpider(scrapy.Spider):
    name = 'kinopoisk_popular'


    def start_requests(self):
        start_url = 'https://www.kinopoisk.ru/lists/movies/popular/'
        yield scrapy.Request(url=get_proxy_url(start_url), callback=self.parse)


    def parse(self, response):
        for film in response.css('div.styles_root__ti07r'):
            yield {
                'ranking_position': film.css('.styles_position__TDe4E::text').get(),
                'russian_title': film.css('.styles_mainTitle__IFQyZ::text').get(),
                'english_title': film.css('.desktop-list-main-info_secondaryTitle__ighTt::text').get(),
                'release_year': film.css('.desktop-list-main-info_secondaryText__M_aus').re_first(r'\d{4}'),
                'kinopoisk_value': film.css('.styles_kinopoiskValue__9qXjg::text').get(),
            }

        next_page = response.css('a.styles_end__aEsmB.styles_start__UvE6T ::attr(href)').get()
        if next_page:
            next_page_url = 'https://www.kinopoisk.ru/' + next_page
            yield response.follow(get_proxy_url(next_page_url), callback=self.parse)

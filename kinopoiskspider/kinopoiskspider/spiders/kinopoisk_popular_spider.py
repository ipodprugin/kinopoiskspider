import scrapy


class KinopoiskPopularSpider(scrapy.Spider):
    name = 'kinopoisk_popular'
    start_urls = ['https://www.kinopoisk.ru/lists/movies/popular/']
    custom_settings = dict(
        DOWNLOADER_MIDDLEWARES={
        'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
        'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
        'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
        'scrapy_fake_useragent.middleware.RetryUserAgentMiddleware': 401,
        },
        FAKEUSERAGENT_PROVIDERS=[
        'scrapy_fake_useragent.providers.FakeUserAgentProvider',
        'scrapy_fake_useragent.providers.FakerProvider',
        'scrapy_fake_useragent.providers.FixedUserAgentProvider',
        ],
    )

    def parse(self, response):
        for film in response.css('div.styles_root__ti07r'):
            yield {
                'ranking_position': film.css('.styles_position__TDe4E::text').get(),
                'russian_title': film.css('.styles_mainTitle__IFQyZ::text').get(),
                'english_title': film.css('.desktop-list-main-info_secondaryTitle__ighTt::text').get(),
                'release_year': film.css('.desktop-list-main-info_secondaryText__M_aus').re(r'\d{4}')[0],
                'kinopoisk_value': film.css('.styles_kinopoiskValue__9qXjg::text').get(),
            }

        yield from response.follow_all(css='div.styles_root__AT6_5 styles_root__RoFSb a', callback=self.parse)
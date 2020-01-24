from scrapy import (Spider, Request)
from random import choice


def random_select_proxy(proxies=[]):
    return choice(proxies)


class GithubCrawler(Spider):
    """A crawler to extract github data from repositories, wikis and Issues
    To use:
    >>> scrapy runspider github-crawler.py -a keywords='jwt' -a proxies='https://36.89.229.97:35098' -a type='Repositories'
    >>> scrapy runspider github-crawler.py -a keywords='jwt' -a proxies='https://36.89.229.97:35098' -a type='Issues'
    >>> scrapy runspider github-crawler.py -a keywords='jwt' -a proxies='https://36.89.229.97:35098' -a type='Wikis'
    """
    name = 'github_crawler'
    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'urls_github.json'
    }

    def __init__(self, **kwargs):
        """
        Is the class constructor, receives the arguments passed when is executed the data
        """
        self.keywords = kwargs.get('keywords')
        self.proxies = kwargs.get('proxies')
        self.type = kwargs.get('type')
        super(GithubCrawler, self).__init__(**kwargs)

    def start_requests(self):
        """
        Do the request to github use the keywords and the type
        """
        keywords = self.keywords.split(',')
        proxy = random_select_proxy(self.proxies.split(','))
       
        for keyword in keywords:
            url_to_req = f'https://github.com/search?q={keyword}&type={self.type}'
            yield Request(url_to_req, self.parse, headers={"User-Agent": "My UserAgent"}, meta={'proxy': proxy})

    def parse(self, response):
        """
        Process the data extracted from github
        """
        item_selector = '.repo-list-item'
        url_selector = 'a ::attr(href)'
        if self.type == 'Issues':
            item_selector = '.issue-list-item .f4'
            url_selector = 'a ::attr(href)'
        elif self.type == 'Wikis':
            item_selector = '.hx_hit-wiki .f4'
            url_selector = 'a ::attr(href)'

        for repo in response.css(item_selector):
            url_item = f"https://github.com{repo.css(url_selector).extract_first()}"
            if self.type == 'Repositories':
                get_repository_data = Request(url_item, callback=self.parse_repository_data)
                get_repository_data.cb_kwargs['url_repo'] = url_item

                yield get_repository_data
            else:
                yield {
                    'url': url_item,
                }

    def parse_repository_data(self, response, url_repo):
        """
        If the argument type is Repositories, this function attach data from each repository
        """
        owner = response.css('a[rel=author]::text').get()
        language_stats_selector = '.repository-lang-stats-numbers li'
        language_stats = {}
        for lss in response.css(language_stats_selector):
            language = lss.css('span.lang::text').get()
            percent = lss.css('span.percent::text').get()
            language_stats[language] = percent

        yield {
            'url': url_repo,
            'extra': {
                "owner": owner,
                "language_stats": language_stats
            }
        }

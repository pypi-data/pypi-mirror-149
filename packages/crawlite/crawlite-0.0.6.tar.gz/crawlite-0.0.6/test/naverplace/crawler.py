
from mimetypes import init
from parso import parse
from crawlite import BaseCrawler, urlpattern,  urlrender
from crawlite.utils.urls import urljoin

from .payloaders import gen_naver_place_comment_payloader
from .extractors import place_detail
from . import settings

COUNT_PER_PAGE = 100





class NaverPlaceCralwer(BaseCrawler):
    HEADERS = {
        'content-type': 'application/json',
    }
    
    def __init__(self, **kwargs):
        super().__init__(settings=settings, **kwargs)


class NaverPlaceSearch(NaverPlaceCralwer):
    urlorders = [
        urlrender(
            'https://map.naver.com/v5/api/instantSearch',
            fields=['coords', 'query'], parser='naver_place_search_parser',
            urlrenderer='naver_place_urlrenderer', name='naver_place_search'
        )
    ]

    def __init__(self, search, **kwargs):
        super().__init__(**kwargs)
        self.search = search
    
    def naver_place_urlrenderer(self):
        yield {'coords': '37.52725,126.9682994', 'query': self.search}

    def naver_place_search_parser(self, response):
        for place in response.json()['place']:
            print(place)


class NaverPlaceDetail(BaseCrawler):

    urlorders = [
        urlrender('https://pcmap.place.naver.com/restaurant/', urlrenderer='naver_place_detail_urlrenderer',
            parser='naver_place_detail_parser', extractor=place_detail,
            name='naver_place_detail'
        )
    ]

    def __init__(self, place_id, **kwargs):
        super().__init__(settings=settings, **kwargs)
        self.place_id = place_id


    def naver_place_detail_urlrenderer(self, url):
        yield urljoin(url, self.place_id)

    def naver_place_detail_parser(self, response, parsed):
        print(parsed)


class NaverPlaceReview(NaverPlaceCralwer):

    urlorders = [
        urlrender(
            'https://pcmap-api.place.naver.com/graphql',
            payloader='naver_place_payloader',
            parser='naver_place_parser', name='naver_place'

        )
    ]

    def __init__(self, place_id, page=-1, **kwargs):
        super().__init__(**kwargs)
        self.place_id = place_id
        self.page = page
        self.total = 0

    def naver_place_payloader(self):
        if self.page == -1:
            return gen_naver_place_comment_payloader(place_id=self.place_id, page=1, count_per_page=1)
        else:
            return gen_naver_place_comment_payloader(place_id=self.place_id, page=self.page, count_per_page=COUNT_PER_PAGE)
        
    
    def naver_place_parser(self, response):
        if data:= response.json():
            data = data[0]['data']
            reviews = data['visitorReviews']
            
            items = reviews['items']
            self.total = reviews['total']
            records = []
            for row in items:
                tags = []
                for taginfo in row['votedKeywords']:
                    tag = taginfo['displayName']
                    tags.append(tag)
                
                record = dict(
                    place_id=self.place_id,
                    author_name = row['author']['nickname'],
                    author_id = row['author']['id'],
                    content = row['body'],
                    visit_count = row['visitCount'],
                    visited = row['visited'],
                    published = row['created'],
                    place_name = row['businessName'],
                    tags=','.join(tags)
                )
                print(record)
                # yield record



def get_place_review_page_count(place_id):
    npd = NaverPlaceReview(place_id=place_id)
    npd.crawl()
    return npd.total // COUNT_PER_PAGE + 1


def crawl_place_review(place_id, page):
    npd = NaverPlaceReview(place_id=place_id)
    npd.crawl()
    



def test_place(**kwargs):
    kfc = NaverPlaceReview(place_id='1564510427', page=1)
    kfc.crawl(kwargs)


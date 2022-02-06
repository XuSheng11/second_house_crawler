from models.seconhouse_model import GuangZhouRegion

from pony.orm import select, db_session
from scrapy.spiders import Spider
from scrapy import Request


class CommunitySpider(Spider):
    name = 'community_spider'
    allowed_domains = ['gz.lianjia.com']
    url = 'https://gz.lianjia.com/xiaoqu/'

    @db_session
    def get_sql_result(self):
        results = [region for region in select(r.region_py for r in GuangZhouRegion)]
        return results

    def start_requests(self):
        for region in ['tianhe']:
            print(region)
            yield Request(url=self.url + region, callback=self.parse_community_list)

    def parse_community_list(self, response):
        urls = response.xpath('//div[@class="page-box fr"]/div/a/@href').get()
        print(urls)
        for url in urls:
            yield Request(url=url, callback=self.parse_community_list)

    def parse_community(self):
        pass

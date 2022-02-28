from models.seconhouse_model import GuangZhouSecondHouseCommonInfo,GuangZhouCommunityInfo
from crawler.spiders import LianJiaSpider
from crawler.items import CommunityCrawlerItem

from pony.orm import select, db_session
from scrapy import Request


class CommunitySpider(LianJiaSpider):
    name = 'community_spider'
    url = 'https://gz.lianjia.com/xiaoqu'

    @db_session
    def send_tasks(self):
        results = []
        for community in select(c.community_id for c in GuangZhouSecondHouseCommonInfo):
            if not GuangZhouCommunityInfo.get(community_id=community):
                results.append(community)
        return results

    def start_requests(self):
        for community in self.send_tasks():
            yield Request(url='%s/%s/' %(self.url, community), callback=self.parse_community)

    def parse_community(self, response):
        item = CommunityCrawlerItem()
        item['community_id'] = self.from_url(response.request.url)
        item['name'] = response.xpath('//h1[@class="detailTitle"]/text()').get()
        item['address'] = response.xpath('//div[@class="detailDesc"]/text()').get()
        item['district_cn'] = response.xpath('//div[@class="fl l-txt"]/a[3]/text()').get()[:-2]
        item['region_cn'] = response.xpath('//div[@class="fl l-txt"]/a[4]/text()').get()[:-2]
        item['unit_price'] = response.xpath('//span[@class="xiaoquUnitPrice"]/text()').get()

        labels = response.xpath('//span[@class="xiaoquInfoLabel"]//text()').extract()
        contents = response.xpath('//span[@class="xiaoquInfoContent"]//text()').extract()
        if labels:
            item['features'] = {}
            for i in range(len(labels)):
                item['features'][labels[i]] = contents[i].strip()

        item['pictures'] = response.xpath('//ol[@id="overviewThumbnail"]/li/@data-src').extract()
        yield item

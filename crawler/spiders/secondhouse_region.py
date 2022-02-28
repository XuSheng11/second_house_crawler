import logging
import json

from crawler.spiders import LianJiaHouseSpider

from scrapy import Request
from pony.orm import db_session
from models.seconhouse_model import GuangZhouRegion


class SecondHouseSpiderRegion(LianJiaHouseSpider):
    name = 'secondhouse_region'

    @db_session
    def send_tasks(self):
        # regions = ['lujing']
        # 天河区所有的区域，使用lambda进行筛选
        regions = [region.region_py for region in GuangZhouRegion.select(lambda r: r.district_py == 'huadou' or r.district_py=='nansha')]
        # regions = [region.region_py for region in select(r for r in GuangZhouRegion)]

        return regions

    def start_requests(self):
        """
        发起请求，scrapy调度器在这里获取请求信息
        需重写
        :return:
        """

        tasks = self.send_tasks()
        for region in tasks:
            yield Request(
                url='%s/%s/' % (self.url, region),
                callback=self.parse_first_page,
                meta={'item': region}
            )

    def parse_first_page(self, response):
        """
        解析特殊房源列表第一页，获取房源数目
        :param response:
        :return:
        """
        meta = response.meta
        item = meta['item']
        # 获取页数信息
        page_data = response.xpath('//div[@class="page-box house-lst-page-box"]/@page-data').get()
        total_page = 1
        if page_data:
            page_data = json.loads(page_data)
            total_page = page_data['totalPage']
        logging.info('%s has totalPage %s' % (item, total_page))

        # 先将第一页的进行抓取解析
        urls = response.xpath('//ul[@class="sellListContent"]/li/a/@href').extract()
        for url in urls:
            yield Request(url=url, callback=self.parse_house)

        # 然后根据页数，将剩下的统一进行转化抓取解析
        for page in range(2, total_page + 1):
            yield Request(
                url='%s/%s/pg%d/' % (self.url, item, page),
                callback=self.parse_house_list,
            )

    def parse_house_list(self, response):
        """
        解析房源列表
        :param response: 响应
        :return:
        """
        urls = response.xpath('//ul[@class="sellListContent"]/li/a/@href').extract()
        for url in urls:
            yield Request(url=url, callback=self.parse_house)

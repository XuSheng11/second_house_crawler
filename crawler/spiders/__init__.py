import logging
import json
import re

from crawler.items import SecondHouseCommonInfoItem, SecondHouseAddressInfoItem, SecondHouseSpecialInfoItem

from scrapy.spiders import Spider
from scrapy import Request


class SecondHouseSpider(Spider):
    allowed_domains = ['gz.lianjia.com']
    url = 'https://gz.lianjia.com/ershoufang'

    def send_tasks(self):
        """
        从数据库获取信息（地铁战，区域）发起任务，在子类中重写
        :return:
        """
        return {}

    def start_requests(self):
        """
        发起请求，scrapy调度器在这里获取请求信息
        :return:
        """
        task = self.send_tasks()
        type = task.get('type')
        meta = task.get('meta')
        for item in meta:
            yield Request(
                url='%s/%s/' % (self.url, item),
                callback=self.parse_first_page,
                meta={'item': item, 'type': type}
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
            yield Request(url=url, callback=self.parse_house, meta=meta)

        # 然后根据页数，将剩下的统一进行转化抓取解析
        for page in range(2, total_page + 1):
            yield Request(
                url='%s/%s/pg%d/' % (self.url, item, page),
                callback=self.parse_house_list,
                meta=meta
            )

    def parse_house_list(self, response):
        """
        解析房源列表
        :param response: 响应
        :return:
        """
        urls = response.xpath('//ul[@class="sellListContent"]/li/a/@href').extract()
        for url in urls:
            yield Request(url=url, callback=self.parse_house, meta=response.meta)

    def parse_house(self, response):
        """
        解析房源信息
        :param response: 响应
        :return: 返回item给pipeline处理，进行存储
        """
        house_id = response.request.url.split('/')[-1][:-5]
        common_info = self.parse_common_info(response=response, house_id=house_id)
        address_info = self.parse_address_info(response=response, house_id=house_id)
        special_info = self.parse_special_info(response=response, house_id=house_id)
        yield common_info
        yield address_info
        yield special_info

    def parse_address_info(self, response, house_id):
        """
        解析房源地址信息
        :param response: 响应
        :return: scrapy 房源地址信息item
        """
        meta = response.meta
        type = meta['type']
        address_info = SecondHouseAddressInfoItem()
        address_info['house_id'] = house_id
        district_url = response.xpath('//div[@class="areaName"]/span[@class="info"]/a[1]/@href').get()
        address_info['district_py'] = self.from_url(district_url)
        address_info['district_cn'] = response.xpath('//div[@class="areaName"]/span[@class="info"]/a[1]/text()').get()
        address_info['region_cn'] = response.xpath('//div[@class="areaName"]/span[@class="info"]/a[2]/text()').get()
        if type == 'region':
            address_info['region_py'] = meta['item']
            station_url = response.xpath('//div[@class="areaName"]/a/@href').get()
            if station_url:
                address_info['station_id'] = self.from_url(station_url)
                address_info['subway_id'] = address_info['station_id'].split('s')[0]
        else:
            address_info['subway_id'] = meta['item'].split('s')[0]
            address_info['station_id'] = meta['item']
            region_url = response.xpath('//div[@class="areaName"]/span[@class="info"]/a[2]/@href').get()
            address_info['region_py'] = self.from_url(region_url)
        return address_info

    def parse_common_info(self, response, house_id):
        """
        解析房源普通信息
        :param response: 响应
        :return: scrapy 房源普通信息item
        """
        common_info = SecondHouseCommonInfoItem()
        common_info['house_id'] = house_id
        common_info['elevator'] = response.xpath(
            '//div[@class="base"]/div[@class="content"]/ul/li[11]/text()').get()
        common_info['title'] = response.xpath('//div[@class="title"]/h1/text()').get()
        common_info['direction'] = response.xpath(
            '//div[@class="houseInfo"]/div[@class="type"]/div[@class="mainInfo"]/text()').get()
        floor_info = response.xpath(
            '//div[@class="houseInfo"]/div[@class="room"]/div[@class="subInfo"]/text()').get()
        floor_num = re.findall('\d{1,}',floor_info)
        if floor_num:
            common_info['floor_num'] = floor_num
            common_info['floor_height'] = floor_info.split('/')[0]
        common_info['floor'] = response.xpath(
            '//div[@class="houseInfo"]/div[@class="room"]/div[@class="subInfo"]/text()').re('\d{1,}')[0]
        common_info['community'] = response.xpath('//div[@class="communityName"]/a[1]/text()').get()
        community_url = response.xpath('//div[@class="communityName"]/a[1]/@href').get()
        common_info['community_id'] = self.from_url(community_url)
        common_info['layout'] = response.xpath(
            '//div[@class="houseInfo"]/div[@class="room"]/div[@class="mainInfo"]/text()').get()
        common_info['total_price'] = response.xpath(
            '//div[@class="price "]/span[@class="total"]/text()').get()
        common_info['unit_price'] = response.xpath(
            '//div[@class="unitPrice"]/span[@class="unitPriceValue"]/text()').get()
        common_info['renovation'] = response.xpath(
            '//div[@class="houseInfo"]/div[@class="type"]/div[@class="subInfo"]/text()').get()[-2:]
        common_info['size'] = response.xpath(
            '//div[@class="houseInfo"]/div[@class="area"]/div[@class="mainInfo"]/text()').get()[:-2]
        year = response.xpath('//div[@class="houseInfo"]/div[@class="area"]/div[2]/text()').get()[:4]
        if year.isdigit():
            common_info['year'] = year
        return common_info

    def parse_special_info(self, response, house_id):
        """
        解析房源特殊信息
        :param response: 响应
        :return: scrapy 房源特殊信息item
        """
        # 房源布局的详细信息
        special_info = SecondHouseSpecialInfoItem()
        special_info['house_id'] = house_id
        info_list = response.xpath('//div[@class="col"]/text()').extract()
        if info_list:
            special_info['layout_detail'] = [
                {
                    'name': info_list[i],
                    'size': info_list[i + 1],
                    'direction': info_list[i + 2],
                    'window': info_list[i + 3],
                }
                for i in range(0, len(info_list), 4)
            ]

        # 房源特色信息
        text = response.xpath('//div[@class="introContent showbasemore"]/div[2]/text()').get()
        if text != '暂无房源介绍':
            names = response.xpath('//div[@class="baseattribute clear"]/div[1]/text()').extract()
            contents = response.xpath('//div[@class="baseattribute clear"]/div[2]/text()').extract()
            contents = [content.strip() for content in contents]
            special_info['features'] = {}
            for i in range(len(names)):
                special_info['features'][names[i]] = contents[i]

        # 房源照片信息
        special_info['pictures'] = {}
        rooms = response.xpath('//div[@class="content-wrapper housePic"]//span//text()').extract()
        images = response.xpath('//div[@class="content-wrapper housePic"]//img//@src').extract()
        for i in range(len(rooms)):
            special_info['pictures'][rooms[i]] = images[i]

        return special_info

    def from_url(self, url):
        """
        从链家url获取相关信息
        :param url:
        :return: 地区id，地铁线路id
        """
        id = url.split('/')[-2]
        return id

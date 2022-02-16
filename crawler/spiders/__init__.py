import re

import scrapy

from crawler.items import SecondHouseCommonInfoItem, SecondHouseSpecialInfoItem


class LianJiaSpider(scrapy.Spider):
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
        需重写
        :return:
        """

    def from_url(self, url):
        """
        从链家url获取相关信息
        :param url:
        :return: 地区id，地铁线路id
        """
        id = url.split('/')[-2]
        return id


class LianJiaHouseSpider(LianJiaSpider):
    def parse_house(self, response):
        """
        解析房源信息
        :param response: 响应
        :return: 返回item给pipeline处理，进行存储
        """
        house_id = response.request.url.split('/')[-1][:-5]
        common_info = self.parse_common_info(response=response, house_id=house_id)
        special_info = self.parse_special_info(response=response, house_id=house_id)
        yield common_info
        yield special_info

    def parse_common_info(self, response, house_id):
        """
        解析房源普通信息
        :param response: 响应
        :return: scrapy 房源普通信息item
        """
        common_info = SecondHouseCommonInfoItem()
        common_info['house_id'] = house_id
        common_info['type'] = response.xpath('//div[@class="transaction"]//ul/li[4]/span[2]/text()').get()
        cover = response.xpath('//div[@class="content-wrapper housePic"]//img//@src').get()
        if cover:
            common_info['cover'] = cover.replace('710x400.jpg','296x216.jpg')
        elevator = response.xpath('//div[@class="base"]/div[@class="content"]/ul/li[11]/text()').get()
        if elevator:
            common_info['elevator'] = elevator
        common_info['title'] = response.xpath('//div[@class="title"]/h1/text()').get()
        common_info['direction'] = response.xpath(
            '//div[@class="houseInfo"]/div[@class="type"]/div[@class="mainInfo"]/text()').get()
        floor_info = response.xpath('//div[@class="houseInfo"]/div[@class="room"]/div[@class="subInfo"]/text()').get()
        floor_num = re.findall('\d{1,}', floor_info)
        if floor_num:
            common_info['floor_num'] = floor_num[0]
            common_info['floor_height'] = floor_info.split('/')[0]
        common_info['community'] = response.xpath('//div[@class="communityName"]/a[1]/text()').get()
        community_url = response.xpath('//div[@class="communityName"]/a[1]/@href').get()
        common_info['community_id'] = self.from_url(community_url)
        common_info['layout'] = response.xpath(
            '//div[@class="houseInfo"]/div[@class="room"]/div[@class="mainInfo"]/text()').get()
        total_price = response.xpath(
            '//div[@class="price "]/span[@class="total"]/text()').get()
        if total_price:
            common_info['total_price'] = round(float(total_price))
        common_info['unit_price'] = response.xpath(
            '//div[@class="unitPrice"]/span[@class="unitPriceValue"]/text()').get()
        common_info['renovation'] = response.xpath(
            '//div[@class="houseInfo"]/div[@class="type"]/div[@class="subInfo"]/text()').get()[-2:]
        common_info['size'] = response.xpath(
            '//div[@class="houseInfo"]/div[@class="area"]/div[@class="mainInfo"]/text()').get()[:-2]
        year = response.xpath('//div[@class="houseInfo"]/div[@class="area"]/div[2]/text()').get()[:4]
        if year.isdigit():
            common_info['year'] = year
        # 解析地址信息
        district_url = response.xpath('//div[@class="areaName"]/span[@class="info"]/a[1]/@href').get()
        common_info['district_py'] = self.from_url(district_url)
        common_info['district_cn'] = response.xpath('//div[@class="areaName"]/span[@class="info"]/a[1]/text()').get()
        common_info['region_cn'] = response.xpath('//div[@class="areaName"]/span[@class="info"]/a[2]/text()').get()

        region_url = response.xpath('//div[@class="areaName"]/span[@class="info"]/a[2]/@href').get()
        common_info['region_py'] = self.from_url(region_url)
        station_url = response.xpath('//div[@class="areaName"]/a/@href').get()
        if station_url:
            common_info['station_id'] = self.from_url(station_url)
            common_info['subway_id'] = common_info['station_id'].split('s')[0]
        return common_info

    def parse_special_info(self, response, house_id):
        """
        解析房源特殊信息
        :param response: 响应
        :return: scrapy 房源特殊信息item
        """

        special_info = SecondHouseSpecialInfoItem()
        special_info['house_id'] = house_id
        # 房源基本属性
        labels = response.xpath('//div[@class="base"]//ul/li//span[1]/text()').extract()
        contents = response.xpath('//div[@class="base"]//ul/li/text()').extract()
        if labels:
            special_info['base'] = {}
            for i in range(len(labels)):
                special_info['base'][labels[i]] = contents[i].strip()

        # 房源布局的详细信息
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
            special_info['features'] = {}
            for i in range(len(names)):
                special_info['features'][names[i]] = contents[i].strip()

        # 房源照片信息
        rooms = response.xpath('//div[@class="content-wrapper housePic"]//span//text()').extract()
        images = response.xpath('//div[@class="content-wrapper housePic"]//img//@src').extract()
        if rooms:
            special_info['pictures'] = {}
            for i in range(len(rooms)):
                special_info['pictures'][rooms[i]] = images[i]

        # 房源交易属性信息
        labels = response.xpath('//div[@class="transaction"]//ul/li//span[1]/text()').extract()
        contents = response.xpath('//div[@class="transaction"]//ul/li//span[2]/text()').extract()
        if labels:
            special_info['trade'] = {}
            for i in range(len(labels)):
                special_info['trade'][labels[i]] = contents[i].strip()
        return special_info

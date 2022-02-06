import scrapy


class SecondHouseAddressInfoItem(scrapy.Item):
    house_id = scrapy.Field()
    district_py = scrapy.Field()
    district_cn = scrapy.Field()
    region_cn = scrapy.Field()
    region_py = scrapy.Field()
    subway_id = scrapy.Field()
    station_id = scrapy.Field()


class SecondHouseCommonInfoItem(scrapy.Item):
    house_id = scrapy.Field()
    title = scrapy.Field()
    type = scrapy.Field()
    direction = scrapy.Field()
    elevator = scrapy.Field()
    floor_num = scrapy.Field()
    floor_height = scrapy.Field()
    community = scrapy.Field()
    community_id = scrapy.Field()
    layout = scrapy.Field()
    total_price = scrapy.Field()
    unit_price = scrapy.Field()
    renovation = scrapy.Field()
    size = scrapy.Field()
    year = scrapy.Field()


class SecondHouseSpecialInfoItem(scrapy.Item):
    house_id = scrapy.Field()
    features = scrapy.Field()
    layout_detail = scrapy.Field()
    pictures = scrapy.Field()
    trade = scrapy.Field()


class CommunityCrawlerItem(scrapy.Item):
    pass

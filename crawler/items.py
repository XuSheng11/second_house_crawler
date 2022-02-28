import scrapy


class SecondHouseCommonInfoItem(scrapy.Item):
    house_id = scrapy.Field()
    title = scrapy.Field()
    cover = scrapy.Field()
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
    district_cn = scrapy.Field()
    region_cn = scrapy.Field()
    subway_id = scrapy.Field()
    station_id = scrapy.Field()


class SecondHouseSpecialInfoItem(scrapy.Item):
    house_id = scrapy.Field()
    features = scrapy.Field()
    layout_detail = scrapy.Field()
    pictures = scrapy.Field()
    trade = scrapy.Field()
    base = scrapy.Field()


class CommunityCrawlerItem(scrapy.Item):
    community_id = scrapy.Field()
    name = scrapy.Field()
    address = scrapy.Field()
    district_cn = scrapy.Field()
    region_cn = scrapy.Field()
    unit_price = scrapy.Field()
    features = scrapy.Field()
    pictures = scrapy.Field()

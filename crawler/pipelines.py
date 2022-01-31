from crawler.items import SecondHouseCommonInfoItem, SecondHouseSpecialInfoItem, SecondHouseAddressInfoItem
from models.seconhouse_model import GuangZhouSecondHouseCommonInfo, GuangZhouSecondHouseSpecialInfo, \
    GuangZhouSecondHouseAddressInfo


class SecondHouseCrawlerPipeline:
    def process_item(self, item, spider):
        if isinstance(item, SecondHouseCommonInfoItem):
            pass
        return item

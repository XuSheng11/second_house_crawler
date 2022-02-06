import logging

from crawler.items import SecondHouseCommonInfoItem, SecondHouseSpecialInfoItem
from models.seconhouse_model import GuangZhouSecondHouseCommonInfo, GuangZhouSecondHouseSpecialInfo, \
    GuangZhouSecondHouseAddressInfo, db

from pony.orm import db_session


class SecondHouseCrawlerPipeline:
    @db_session
    def process_item(self, item, spider):
        data = dict(item)
        if isinstance(item, SecondHouseCommonInfoItem):
            if not GuangZhouSecondHouseCommonInfo.get(house_id=data['house_id']):
                GuangZhouSecondHouseCommonInfo(**data)
                logging.info('The common_info of Second house %s has been stored' % (data['house_id']))
        elif isinstance(item, SecondHouseSpecialInfoItem):
            if not GuangZhouSecondHouseSpecialInfo.get(house_id=data['house_id']):
                GuangZhouSecondHouseSpecialInfo(**data)
                logging.info('The speccial_info of Second house %s has been stored' % (data['house_id']))
        else:
            if not GuangZhouSecondHouseAddressInfo.get(house_id=data['house_id']):
                # 当subway_id 为空时会报外键出错（会插入‘’空字符串），只能通过原始sql插入（不插入subway_id）
                table = 'guangzhou_secondhouse_address_info'
                fields = ','.join(data.keys())
                contents = ','.join('%r' % (value) for value in data.values())
                sql = 'insert into  %s (%s) values(%s)' % (table, fields, contents)
                db.execute(sql=sql)
                logging.info('The address_info of Second house %s has been stored' % (data['house_id']))

        return item

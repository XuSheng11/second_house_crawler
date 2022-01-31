from models.seconhouse_model import GuangZhouSubwayStation

from crawler.spiders import SecondHouseSpider
from pony.orm import select, db_session


class SubwaySecondHouseSpider(SecondHouseSpider):
    name = 'subway_secondhouse_spider'

    @db_session
    def get_sql_result(self):
        stations = [station for station in select(s.id for s in GuangZhouSubwayStation)]
        task = {
            'type': 'subway',
            'meta': stations,
        }
        return task

from models.seconhouse_model import GuangZhouRegion

from crawler.spiders import SecondHouseSpider
from pony.orm import select, db_session


class RegionSecondHouseSpider(SecondHouseSpider):
    name = 'region_secondhouse_spider'

    @db_session
    def send_tasks(self):
        regions = ['zhujiangxinchengxi']
        # regions = [region for region in select(r.region_py for r in GuangZhouRegion)]
        task = {
            'type': 'region',
            'meta': regions,
        }
        return task

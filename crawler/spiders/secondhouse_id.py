from models.seconhouse_model import db
from crawler.spiders import LianJiaHouseSpider

from pony.orm import db_session
from scrapy import Request


class SecondHouseIdSpider(LianJiaHouseSpider):
    name = 'secondhouse_id'

    @db_session
    def send_tasks(self):
        sql = 'select c.house_id from guangzhou_secondhouse_common_info c left join guangzhou_secondhouse_address_info a on c.house_id=a.house_id where a.house_id is NULL'
        results = db.execute(sql=sql).fetchall()
        task = [house[0] for house in results]
        print(task)
        return task

    def start_requests(self):
        """
        发起请求，scrapy调度器在这里获取请求信息
        需重写
        :return:
        """
        # tasks = ['108402450730','108403025890']
        tasks = self.send_tasks()
        for house_id in tasks:
            url = 'https://gz.lianjia.com/ershoufang/%s.html' % (house_id)
            yield Request(url=url, callback=self.parse_house)

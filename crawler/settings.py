import pymysql
BOT_NAME = 'crawler'

SPIDER_MODULES = ['crawler.spiders']
NEWSPIDER_MODULE = 'crawler.spiders'

ROBOTSTXT_OBEY = False

MYSQL_SETTINGS = {
    "database": "lianjia",
    "user": "root",
    "password": "0427shun",
    "host": "127.0.0.1",
    "port": 3306,
    "charset":"utf8mb4"
}
connect = pymysql.connect(**MYSQL_SETTINGS)

DOWNLOADER_MIDDLEWARES = {
    'crawler.middlewares.RandomUserAgentMiddleware': 543,
    'crawler.middlewares.ProxyMiddleware': 542,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None
}
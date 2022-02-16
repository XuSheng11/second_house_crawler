import pymysql

BOT_NAME = 'crawler'

SPIDER_MODULES = ['crawler.spiders']
NEWSPIDER_MODULE = 'crawler.spiders'

ROBOTSTXT_OBEY = False

# 控制爬取速度
DOWNLOAD_DELAY = 0.45
CONCURRENT_REQUESTS = 96

# 日志等级
LOG_LEVEL = "INFO"

MYSQL_SETTINGS = {
    "database": "lianjia",
    "user": "root",
    "password": "0427shun",
    "host": "127.0.0.1",
    "port": 3306,
    "charset": "utf8mb4"
}
connect = pymysql.connect(**MYSQL_SETTINGS)

DOWNLOADER_MIDDLEWARES = {
    'crawler.middlewares.RandomUserAgentMiddleware': 543,
    'crawler.middlewares.ProxyMiddleware': 542,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None
}

ITEM_PIPELINES = {
    'crawler.pipelines.SecondHouseCrawlerPipeline': 400
}

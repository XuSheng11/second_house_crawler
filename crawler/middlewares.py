from fake_useragent import UserAgent


class RandomUserAgentMiddleware():
    # 随机更换user-agent
    def __init__(self, crawler):
        super(RandomUserAgentMiddleware, self).__init__()
        self.ua = UserAgent()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        def get_ua():
            return getattr(self.ua, 'random')
        request.headers['User-Agent'] = get_ua()

class ProxyMiddleware():
    def process_request(self, request,spider):
        request.meta['proxy'] = 'https://127.0.0.1:7890'


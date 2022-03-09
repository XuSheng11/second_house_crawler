# second_house_crawler
- 爬取广州地区链家二手房代码，使用scrapy框架
- 先运行抓取区域和地铁信息脚本，在启动爬虫
- 启动方式：命令行输入`scrapy crawl 爬虫名`，例如`scrapy crawl secondhouse_id`
- 可配合[二手房web项目](https://github.com/XuSheng11/second_house_web)进行房源展示
### models
使用pony orm来进行数据库实体管理
### scrapy
#### 中间件
- 代理中间件
- 随机UA中间件
- 格式化URL中间件
#### 管道
- MySQL储存
#### 项目item
- 二手房普通信息
- 二手房特色信息
- 小区信息
### 爬虫
- 二手房信息（根据区域）
- 二手房信息（id）
- 小区信息
### 抓取脚本
- 地铁信息
- 区域信息

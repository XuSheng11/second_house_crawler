from crawler.settings import MYSQL_SETTINGS

from pony.orm import Database
from pony.orm import Optional
from pony.orm import PrimaryKey
from pony.orm import Required
from pony.orm import set_sql_debug

db = Database()
db.bind(
    provider='mysql',
    host=MYSQL_SETTINGS['host'],
    port=MYSQL_SETTINGS['port'],
    user=MYSQL_SETTINGS['user'],
    passwd=MYSQL_SETTINGS['password'],
    db=MYSQL_SETTINGS['database']
)
set_sql_debug(False)


# 广州区域表
class GuangZhouRegion(db.Entity):
    _table_ = 'guangzhou_region'
    region_py = PrimaryKey(str)
    region_cn = Required(str)
    district_py = Required(str)


# 广州地铁站表
class GuangZhouSubwayStation(db.Entity):
    _table_ = 'guangzhou_subway_station'
    id = PrimaryKey(str)
    name = Required(str)
    subway_id = Required(str)


# # 广州二手房普通信息表
# class GuangZhouSecondHouseCommonInfo(db.Entity):
#     # _table_ = 'guangzhou_secondhouse_common_info'
#     # house_id = PrimaryKey(int)
#     pass
#
# # 广州二手房特殊信息表
# class GuangZhouSecondHouseSpecialInfo(db.Entity):
#     pass
#
#
# # 广州二手房地址信息表
# class GuangZhouSecondHouseAddressInfo(db.Entity):
#     pass


db.generate_mapping(create_tables=False)

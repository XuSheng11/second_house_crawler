from crawler.settings import MYSQL_SETTINGS

from pony.orm import Database
from pony.orm import Optional
from pony.orm import PrimaryKey
from pony.orm import Required
from pony.orm import Json
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
set_sql_debug(debug=False)


# 广州区域表
class GuangZhouRegion(db.Entity):
    _table_ = 'guangzhou_region'
    region_py = Required(str)
    region_cn = Required(str)
    district_py = Required(str)
    PrimaryKey(region_py, district_py)


# 广州地铁站表
class GuangZhouSubwayStation(db.Entity):
    _table_ = 'guangzhou_subway_station'
    id = PrimaryKey(str)
    name = Required(str)
    subway_id = Required(str)


# 广州二手房普通信息表
class GuangZhouSecondHouseCommonInfo(db.Entity):
    _table_ = 'guangzhou_secondhouse_common_info'
    house_id = PrimaryKey(str)
    title = Required(str)
    type = Required(str)
    direction = Optional(str)
    elevator = Optional(str)
    floor_num = Optional(int)
    floor_height = Optional(str)
    community = Required(str)
    community_id = Required(str)
    layout = Required(str)
    total_price = Optional(int)
    unit_price = Optional(int)
    renovation = Optional(str)
    size = Optional(float)
    year = Optional(int)


# 广州二手房特殊信息表
class GuangZhouSecondHouseSpecialInfo(db.Entity):
    _table_ = 'guangzhou_secondhouse_special_info'
    house_id = PrimaryKey(str)
    features = Optional(Json)
    layout_detail = Optional(Json)
    pictures = Optional(Json)
    trade = Optional(Json)


# 广州二手房地址信息表
class GuangZhouSecondHouseAddressInfo(db.Entity):
    _table_ = 'guangzhou_secondhouse_address_info'
    house_id = PrimaryKey(str)
    district_py = Required(str)
    district_cn = Required(str)
    region_cn = Required(str)
    region_py = Required(str)
    station_id = Optional(str)
    subway_id = Optional(str)


db.generate_mapping(create_tables=False)

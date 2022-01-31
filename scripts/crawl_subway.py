"""
抓取广州地铁的信息
"""
from crawler.settings import connect

import requests
from lxml import etree

cursor = connect.cursor()
cursor.execute('select id from guangzhou_subway')
result = cursor.fetchall()
for subway_id in result:
    print(subway_id)
    response = requests.get('https://gz.lianjia.com/ditiefang/%s/' % (subway_id[0]))
    html = etree.HTML(response.text)
    urls = html.xpath('//div[@data-role="ditiefang"]/div[2]/a/@href')
    station_id = []
    for url in urls:
        station_id.append(url.split('/')[-2])
    station_name = html.xpath('//div[@data-role="ditiefang"]/div[2]/a/text()')
    for i in range(len(station_id)):
        sql = 'insert into guangzhou_subway_station (id,name,subway_id) values (%r,%r,%r)' % (
            station_id[i], station_name[i], subway_id[0])
        print(sql)
        cursor.execute(sql)
connect.commit()
connect.close()
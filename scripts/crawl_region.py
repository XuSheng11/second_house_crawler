"""
抓取广州各个区下的具体区域
"""
from crawler.settings import connect

import requests
from lxml import etree

cursor = connect.cursor()
cursor.execute('select district_py from guangzhou_district')
result = cursor.fetchall()
for district in result:
    print(district)
    response = requests.get('https://gz.lianjia.com/ershoufang/%s/' % (district[0]))
    html = etree.HTML(response.text)
    urls = html.xpath('//div[@data-role="ershoufang"]/div[2]/a/@href')
    region_py = []
    for url in urls:
        region_py.append(url.split('/')[-2])
    region_cn = html.xpath('//div[@data-role="ershoufang"]/div[2]/a/text()')
    for i in range(len(region_py)):
        sql = 'insert into guangzhou_region (region_py,region_cn,district_py) values (%r,%r,%r)' % (
            region_py[i], region_cn[i], district[0])
        print(sql)
        cursor.execute(sql)
connect.commit()
connect.close()

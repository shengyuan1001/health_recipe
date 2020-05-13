#  -*- codeing: utf-8 -*- #
# 作者: bob
# 日期: 2020/4/1
import datetime
import json

from urllib.request import urlopen
from lxml.html import etree
import MySQLdb.cursors
import requests
# Windows使用 结合charom驱动器
# from selenium import webdriver

reponse = requests.get('https://ncov.dxy.cn/ncovh5/view/pneumonia')


def world_epidemic_data():
    browser = webdriver.Chrome()
    browser.get('https://ncov.dxy.cn/ncovh5/view/pneumonia')
    div = browser.find_elements_by_class_name("expandRow___1Y0WD")

    for i in div:
        i.click()
    datas = browser.find_elements_by_xpath(
        '//div[@class="areaBox___Sl7gp themeA___1BO7o numFormat___nZ7U7 flexLayout___1pYge"][2]/div[position()>2 and position()<10]')

    title_list = []
    url_list = []
    for data in datas:
        items = data.find_elements_by_xpath('div[position()>1]')
        for item in items:
            title = item.find_elements_by_xpath('p[@class="subBlock1___3cWXy"]')
            urls = item.find_elements_by_xpath('p[last()]/a[@class="alink___38BGN"]')
            if len(title) == len(urls):
                for i in range(len(title)):
                    title_list.append(title[i].text)
                    url_list.append(urls[i].get_attribute("href"))

    urls_dict = dict(zip(title_list, url_list))
    print(urls_dict)


def get_world_epidemic_json():
    url = 'https://ncov.dxy.cn/ncovh5/view/pneumonia_area?from=dxy&source=&link=&share=&cid=ITA'
    country_dict = {}
    res = urlopen(url)
    if res.status == 200:
        html_content = res.read().decode()  # 获取下载的网页内容
        et_node = etree.HTML(html_content)  # 返回根节点对象
        data = str(et_node.xpath("//body/script[position()=1]/text()")[0])
        data = data.split('=')[-1].split('},')
        for i in range(len(data)):
            if ('"id"' in data[i] or '"provinceName":"中国"' in data[i]) and '"incrVo"' in data[i]:
                text = data[i].strip(' [') + '}}'
                item = json.loads(text)
                country_dict[item['provinceName']] = item
    return country_dict


def dispose_data(item):
    country_dict = {}
    for e, v in item.items():
        data = {
            'name': v['provinceName'],
            'today':
                {
                    'confirm': v['currentConfirmedCount'],
                },
            'total':
                {
                    'name': v['provinceName'],
                    'confirm': v['confirmedCount'],
                    'confirmIncr': v['incrVo']['confirmedIncr'],
                    'suspect': v['suspectedCount'],
                    'dead': v['deadCount'],
                    'deadIncr': v['incrVo']['deadIncr'],
                    'heal': v['curedCount'],
                    'healIncr': v['incrVo']['curedIncr'],
                    # 治愈率、死亡率
                    'deadRate': round((v['deadCount'] / v['confirmedCount']) * 100, 2),
                    'healRate': round((v['curedCount'] / v['confirmedCount']) * 100, 2),
                    'detail_json_url': v['statisticsData'],
                    'date': datetime.datetime.now().strftime('%Y-%m-%d')
                },
            'children': None,
            'incrvo': v['incrVo'],
            'statisticsData': v['statisticsData']
        }
        country_dict[e] = data
    return country_dict


def get_global_data():
    data = get_world_epidemic_json()
    data = dispose_data(data)
    return data


def mysql_save():
    print('正在执行程序，稍等........')
    data = get_global_data()
    conn = MySQLdb.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='Bbb1105711060.',
        db='epidemic_data',
        charset='utf8',
        cursorclass=MySQLdb.cursors.SSCursor
    )
    cur = conn.cursor()
    for e, v in data.items():
        sql = 'select name from epidemic_epidemiccountry where name="{}";'.format(e)
        cur.execute(sql)
        name = cur.fetchone()
        data_dict = v['total']
        if name:
            sql = 'UPDATE epidemic_epidemiccountry SET {} WHERE name="{}";'.format(
                ','.join('{}="{}"'.format(i, data_dict[i]) for i in data_dict), e)
        else:
            sql = 'INSERT INTO epidemic_epidemiccountry ({}) VALUES ({});'.format(
                ','.join('{}'.format(i) for i in data_dict),
                ','.join('"{}"'.format(data_dict[i]) for i in data_dict))
        cur.execute(sql)
        sql = 'select id from epidemic_epidemiccountry where name="{}";'.format(e)
        cur.execute(sql)
        Id = cur.fetchone()[0]
        res = requests.get(v['statisticsData']).json()
        for item in res['data']:
            res_dict = {
                'e_id': Id,
                'name': e,
                'confirm': item['confirmedCount'],
                'confirmIncr': item['confirmedIncr'],
                'suspect': item['suspectedCount'],
                'suspectIncr': item['suspectedCountIncr'],
                'dead': item['deadCount'],
                'deadIncr': item['deadIncr'],
                'heal': item['curedCount'],
                'healIncr': item['curedIncr'],
                # 治愈率、死亡率
                'deadRate': round((item['deadCount'] / item['confirmedCount']) * 100, 2),
                'healRate': round((item['curedCount'] / item['confirmedCount']) * 100, 2),
                'date': item['dateId']
            }
            sql = 'select * from history_epidemic_country where name="{}" and date="{}";'.format(e, res_dict['date'])
            cur.execute(sql)
            sql_data = cur.fetchone()
            # print(sql_data)
            if not sql_data:
                sql = 'INSERT INTO history_epidemic_country ({}) VALUES ({});'.format(
                    ','.join('{}'.format(i) for i in res_dict),
                    ','.join('"{}"'.format(res_dict[i]) for i in res_dict))
                cur.execute(sql)
    cur.close()
    conn.commit()
    print('执行完成！！')


if __name__ == '__main__':
    mysql_save()
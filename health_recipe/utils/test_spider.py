import re
import time
import json
import datetime
import requests
import pymysql
import pandas as pd


class VirusSupervise(object):
    def __init__(self):
        self.url = 'https://3g.dxy.cn/newh5/view/pneumonia?scene=' \
                   '2&clicktime=1579582238&enterid=1579582238&from=timeline&isappinstalled=0'
        self.all_data = list()
        self.host_ip = "localhost"  # 数据库地图
        self.host_user = "root"  # 用户
        self.database = 'epidemic_data'
        self.password = 'buzhidao'  # 数据库密码

    def request_page(self):
        """
        请求页面数据
        """
        res = requests.get(self.url)
        res.encoding = 'utf-8'
        pat0 = re.compile('window.getAreaStat = ([\s\S]*?)</script>')
        data_list = pat0.findall(res.text)
        data = data_list[0].replace('}catch(e){}', '')
        data = eval(data)
        return data

    def deep_spider(self, data, province_name):
        """
        深度提取出标签里详细的数据
        :param data:
        :param province_name:
        :return:
        """
        for temp_data in data:
            self.all_data.append([temp_data["cityName"], temp_data["confirmedCount"], temp_data["curedCount"],
                                  temp_data["deadCount"], province_name, datetime.date.today(),
                                  datetime.datetime.now().strftime('%H:%M:%S')])

    def filtration_data(self):
        """
        过滤数据
        """
        temp_data = self.request_page()
        province_short_names, confirmed_counts, cured_counts, dead_counts = list(), list(), list(), list()
        for i in temp_data:
            province_short_names.append(i['provinceShortName'])  # 省份
            confirmed_counts.append(i['confirmedCount'])  # 确诊
            cured_counts.append(i['curedCount'])  # 治愈
            dead_counts.append(i['deadCount'])  # 死亡
            self.deep_spider(i['cities'], i["provinceShortName"])  # 深度解析数据添加到实例属性中

        all_data = pd.DataFrame(self.all_data, columns=["城市", "确诊", "治愈", "死亡", "省份", "日期", "时间"])
        # print(all_data[all_data["省份"] == "陕西"])
        df = pd.DataFrame()
        df['省份'] = province_short_names
        df['确诊'] = confirmed_counts
        df['治愈'] = cured_counts
        df['死亡'] = dead_counts
        print(df)
        # all_data.to_csv("疫情数据_1.csv", encoding="utf_8_sig")
        return all_data

    def insert_wis_sql(self):
        data = self.filtration_data()

        coon = pymysql.connect(host=self.host_ip, user=self.host_user, password=self.password, database=self.database,
                                    charset="utf8")
        item = pd.read_sql("select cycle from all_data order by id DESC limit 1", coon)["cycle"].to_list()
        if len(item) == 0:
            item = 0
        else:
            item = pd.read_sql("select cycle from all_data order by id DESC limit 1", coon)["cycle"].to_list()[0]
        number = int(item) + 1
        print("正在向阿里云服务器插入数据: ", number)
        cursor = coon.cursor()  # 创建事务
        sql = "insert into all_data(cityName, confirmedCount, curedCount, deadCount, province_name, " \
              "date_info, detail_time, cycle) values(%s, %s, %s, %s, %s, %s, %s, %s)"

        print("正在插入数据...")
        for cityName, confirmedCount, curedCount, deadCount, province_name, date_info, detail_time in zip(data["城市"],
                        data["确诊"], data["治愈"], data["死亡"], data["省份"], data["日期"], data["时间"]):
            cursor.execute(sql, (cityName, confirmedCount, curedCount, deadCount, province_name, date_info, detail_time, number))
            coon.commit()
        print("数据插入完成...")
        cursor.close()
        coon.close()

    def data_analysis(self):
        """
        数据分析返回结果
        :return:
        """
        importance_province = "陕西"  # 你所在的省市(注意数据库里是否有此数据)
        importance_city = "西安"  # 你所在的城市(同上) result中的需要自己修改
        result = "您好!\n我是你的智能疫情监控机器人ABL\n现在是北京时间: %s %s\n%s\n在十二小时内\n全国内陆" \
                 "30个地区:\n总病例:%s\n全国新增病例:%s\n西安新增病例:%s 积累病例:%s\n陕西积累病例:%s\n下面是新增疫情详细数据:%s疫情期间,注意保护好自己和家" \
                 "人的健康\n如什么问题可以问我哦"  # 时间 天气 昨天时间 今日时间 疫情数据
        coon = pymysql.connect(host=self.host_ip, user=self.host_user, password=self.password,
                               database="epidemic_data",
                               charset="utf8")
        number = pd.read_sql("select cycle from all_data order by id DESC limit 1", coon)["cycle"].to_list()[0]
        data1 = pd.read_sql("select * from all_data where cycle = %s" % number, coon)
        data2 = pd.read_sql("select * from all_data where cycle = %s" % (int(number) - 1), coon)
        now_time = data1.date_info.unique()[0] + " " + data1.detail_time.unique()[0]  # 查询数据收集时间
        week_info = self.get_week_day(datetime.date.today())
        weather = self.get_window()  # 天气数据
        all_num = data1["confirmedCount"].sum()  # 目前总人数
        add_all_num = data1["confirmedCount"].sum() - data2["confirmedCount"].sum()  # 总新增人数

        sx_all = data1[data1["province_name"] == importance_province]["confirmedCount"].sum()
        add_xian = int(data1[data1["cityName"] == importance_city]["confirmedCount"]) - \
                   int(data2[data2["cityName"] == importance_city]["confirmedCount"])  # 西安新增人数
        xian_all = int(data1[data1["cityName"] == importance_city]["confirmedCount"])

        temp_a1 = data1.groupby("province_name")["confirmedCount"].sum()
        temp_a2 = data2.groupby("province_name")["confirmedCount"].sum()
        add_city = (temp_a1 - temp_a2).sort_values(ascending=False)
        add_city = add_city[add_city.values != 0]  # 新增地区及人数
        result_str = "\n"
        for city_name, number in zip(add_city.index.tolist(), add_city.values.tolist()):
            str_data = str(city_name) + "新增病例: " + str(number) + "\n"
            result_str += str_data

        danger_area = data2.groupby("province_name")["confirmedCount"].sum().sort_values(ascending=False)[: 10]
        danger_str = "\n"  # 疫情严重地区可以自己添加
        for city_name, number in zip(danger_area.index.tolist(), danger_area.values.tolist()):
            str_data = str(city_name) + "出现病例: " + str(number) + "\n"
            danger_str += str_data

        result = result % (str(now_time).split(" ")[1], week_info, weather, all_num, add_all_num,
                           add_xian, xian_all, sx_all, result_str)
        coon.close()
        return result

    @staticmethod
    def get_week_day(date):
        week_day = {
            0: '星期一',
            1: '星期二',
            2: '星期三',
            3: '星期四',
            4: '星期五',
            5: '星期六',
            6: '星期日',
        }
        day = date.weekday()  # weekday()可以获得是星期几
        return week_day[day]

    @staticmethod
    def get_window():
        url = "http://api.qingyunke.com/api.php?key=free&appid=0&msg=%E8%A5%BF%E5%AE%89%E5%A4%A9%E6%B0%94"
        response = requests.get(url)
        content = json.loads(response.content.decode())
        if content["result"]:
            return "未获取到天气信息"
        else:
            return content["content"]


if __name__ == '__main__':
    sup = VirusSupervise()
    # sup.insert_wis_sql()
    print(sup.data_analysis())

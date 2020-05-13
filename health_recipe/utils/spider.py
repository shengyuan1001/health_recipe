import re
import time
import datetime
import redis
import requests
import pymysql
import pandas as pd


class VirusSupervise(object):
    def __init__(self):
        self.url = 'https://3g.dxy.cn/newh5/view/pneumonia?scene=2&clicktime=1579582238&enterid=1579582238&from=timeline&isappinstalled=0'
        self.rumor_url = "https://3g.dxy.cn/newh5/view/pneumonia_rumors?from=dxy"
        self.data_all = list()
        self.red = redis.Redis(host='127.0.0.1', port=6379, db=1)
        self.host_ip = "127.0.0.1"
        self.host_user = "root"  # 数据库用户
        self.database = 'epidemic_data'  # 数据表名
        self.password = 'buzhidao'  # 数据库密码

    def run(self):
        while True:
            self.insert_wis_sql()
            self.data_analysis()
            hour = 3  # 小时
            time.sleep(hour * 3600)

    def request_page(self):
        """
        请求页面数据
        """
        res = requests.get(self.url)
        res.encoding = 'utf - 8'
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
            self.data_all.append([temp_data["cityName"], temp_data["confirmedCount"], temp_data["curedCount"],
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

        data_all = pd.DataFrame(self.data_all, columns=["城市", "确诊", "治愈", "死亡", "省份", "日期", "时间"])
        df = pd.DataFrame()
        df['省份'] = province_short_names
        df['确诊'] = confirmed_counts
        df['治愈'] = cured_counts
        df['死亡'] = dead_counts
        print(df)
        # data_all.to_csv("疫情数据_1.csv", encoding="utf_8_sig")
        return data_all

    def insert_wis_sql(self):
        data = self.filtration_data()

        coon = pymysql.connect(host=self.host_ip, user=self.host_user, password=self.password, database=self.database,
                               charset="utf8")
        item = pd.read_sql("select cycle from data_all order by id DESC limit 1", coon)["cycle"].to_list()
        if len(item) == 0:
            item = 0
        else:
            item = pd.read_sql("select cycle from data_all order by id DESC limit 1", coon)["cycle"].to_list()[0]
        number = int(item) + 1
        print("正在向阿里云服务器插入数据: ", number)
        cursor = coon.cursor()  # 创建事务
        sql = "insert into data_all(cityName, confirmedCount, curedCount, deadCount, province_name, " \
              "date_info, detail_time, cycle) values(%s, %s, %s, %s, %s, %s, %s, %s)"

        print("正在插入数据...")
        for cityName, confirmedCount, curedCount, deadCount, province_name, date_info, detail_time in zip(data["城市"],
                                                                                                          data["确诊"],
                                                                                                          data["治愈"],
                                                                                                          data["死亡"],
                                                                                                          data["省份"],
                                                                                                          data["日期"],
                                                                                                          data["时间"]):
            cursor.execute(sql, (
                cityName, confirmedCount, curedCount, deadCount, province_name, date_info, detail_time, number))
            coon.commit()
        print("数据插入完成...")
        cursor.close()
        coon.close()

    def data_analysis(self):
        """
        数据分析返回结果
        :return:
        """
        print(self.red.flushdb())
        coon = pymysql.connect(host=self.host_ip, user=self.host_user, password=self.password, database=self.database,
                               charset="utf8")
        # 读取所有数据
        data_all = pd.read_sql("select * from data_all", coon)
        # 查询最新一次数据的索引
        number = pd.read_sql("select cycle from data_all order by id "
                             "DESC limit 1", coon)["cycle"].to_list()[0]

        # 查询最新一次的数据
        data1 = data_all[data_all["cycle"] == number]
        print('查询最新一次的数据', data1)
        # 查询距离上一次12小时前的数据
        data2 = data_all[data_all["cycle"] == int(number) - 1]
        print('查询距离上一次12小时前的数据', data2)

        # 1.提取出目前有多少感染的人
        confirmed_all = data1["confirmedCount"].sum()  # 总感染人数 redis.set.confirmed_all
        print('提取出目前有多少感染的人', confirmed_all)
        # 2.提取出今日新增确诊病例
        cured_all = data1["confirmedCount"].sum() - data2["confirmedCount"].sum()  # 今日新增病例数 redis.set.cured_all
        print('提取出今日新增确诊病例', cured_all)
        self.red.set("confirmed_all", int(confirmed_all))
        self.red.set("cured_all", int(cured_all))

        # 3.提取出目前确诊病例最多的城市
        serious_all = data1[["cityName", "confirmedCount"]].sort_values(by="confirmedCount", ascending=False)[0:7]
        print('提取出目前确诊病例最多的城市', serious_all)
        serious_all_index = serious_all["cityName"].tolist()  # redis.serious_all_index
        serious_all_value = serious_all["confirmedCount"].tolist()  # redis.serious_all_value
        [self.red.rpush("serious_index", x) for x in serious_all_index]
        [self.red.rpush("serious_value", x) for x in serious_all_value]

        # 4.提取出今日新增确诊病例的城市
        add_nums = (data1.groupby("province_name")["confirmedCount"].sum() - data2.groupby("province_name")[
            "confirmedCount"].
                    sum()).sort_values(ascending=False)[1:10]  # 因为湖北增长比较多其他数据就显的比较小所以没有计算湖北
        [self.red.rpush("add_nums_index", x) for x in add_nums.index.tolist()]
        [self.red.rpush("add_nums_value", x) for x in add_nums.values.tolist()]

        confirmed_num = data1.groupby("province_name")["confirmedCount"].sum()  # 确诊比例
        print(confirmed_num, '')
        confirmed_num = [confirmed_num["湖北"], (confirmed_num.sum() - confirmed_num["湖北"])]
        [self.red.rpush("confirmed_num", int(x)) for x in confirmed_num]

        deed_num = data1.groupby("province_name")["deadCount"].sum()  # 死亡比例
        deed_num = [deed_num["湖北"], (deed_num.sum() - deed_num["湖北"])]
        [self.red.rpush("deed_num", int(x)) for x in deed_num]

        add_num1 = data1.groupby("province_name")["confirmedCount"].sum()  # 增长比例
        add_num2 = data2.groupby("province_name")["confirmedCount"].sum()
        add_num = (add_num1 - add_num2).sort_values(ascending=False)
        print(add_num.sum())
        print(add_num['湖北'])
        [self.red.rpush("add_nums", int(x)) for x in [add_num["湖北"], add_num.sum() - add_num["湖北"]]]

        '''取出增长趋势图的数据'''
        # 获取每天上午爬去数据的 cycle 索引
        temp_list = [x for x in range(number + 1) if x % 2 != 0]
        # 提取出前12次数据每天上午确诊病例的人数总和
        confirmed_list = [[data_all[data_all["cycle"] == num]["date_info"].unique()[0],
                           data_all[data_all["cycle"] == num]["confirmedCount"].sum()] for num in
                          (temp_list if len(temp_list) <= 12 else temp_list[len(temp_list) - 12:])]
        # 提取出前12次数据每天上午治愈人数总和
        cured_list = [[data_all[data_all["cycle"] == num]["date_info"].unique()[0],
                       data_all[data_all["cycle"] == num]["curedCount"].sum()] for num in
                      (temp_list if len(temp_list) <= 12 else temp_list[len(temp_list) - 12:])]
        # 将数据转换为pandas.DataFrame
        confirmed_temp = pd.DataFrame(confirmed_list, columns=["date", "num"])
        cured_temp = pd.DataFrame(cured_list, columns=["date", "num"])
        # 相隔天数的数据相减得到数据列表【日期，确诊病例每日增长数，治愈病例每日增长数量】
        line_data = [confirmed_temp["date"].apply(lambda x: x.split("-")[-1]).tolist(),
                     (confirmed_temp["num"] - confirmed_temp["num"].shift(1)).tolist(),
                     (cured_temp["num"] - cured_temp["num"].shift(1)).tolist()]

        [self.red.rpush("line_data_date", x) for x in line_data[0]]
        [self.red.rpush("line_data_value1", x) for x in line_data[1]]
        [self.red.rpush("line_data_value2", x) for x in line_data[2]]

        # 康复人数与死亡人数
        bar_num = [data1["curedCount"].sum(), data1["deadCount"].sum()]
        [self.red.rpush("bar_num", int(x)) for x in bar_num]

        # 地图数据
        map_df = data1[["cityName", "confirmedCount"]].sort_values(by="confirmedCount", ascending=False)
        # print(map_df["cityName"].tolist())
        # print((map_df["confirmedCount"] * 0.01).tolist())
        [self.red.rpush("map_index", x) for x in map_df["cityName"].tolist()]
        [self.red.rpush("map_value", x) for x in (map_df["confirmedCount"]).tolist()]


# 如果你是测试直接运行程序就可以，如果你想部署到服务器，
# 注释掉 sup.data_analysis() 使用 sup.run() 程序会每隔 12 个小时运行一次，
# 然后将分析数据存储到 redis
if __name__ == '__main__':
    sup = VirusSupervise()  # 主程序
    sup.insert_wis_sql()
    sup.data_analysis()
    # sup.run()
    # sup.filtration_data()

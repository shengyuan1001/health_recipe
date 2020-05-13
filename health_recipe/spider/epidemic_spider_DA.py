#  -*- codeing: utf-8 -*- #
# 作者: bob
# 日期: 2020/3/31
# 数据来源 [腾讯疫情实时追踪](https://news.qq.com/zt2020/page/feiyan.htm?from=timeline&isappinstalled=0)
# 数据来源 [丁香园·丁香医生](https://ncov.dxy.cn/ncovh5/view/pneumonia)
# 数据来源 [丁香园·丁香医生](国外数据)(https://ncov.dxy.cn/ncovh5/view/pneumonia_area?from=dxy&source=&link=&share=&cid=ITA)

import json
import os

import requests
import pandas as pd
from pyecharts.charts import *
from pyecharts import options as opts
from pyecharts.commons.utils import JsCode
from pyecharts.globals import ThemeType, ChartType
from bs4 import BeautifulSoup

# 获取当前路径
from spider.ncov import get_global_data

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 抓取数据
reponse = requests.get('https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5').json()
data = json.loads(reponse['data'])
# 国内
lastUpdateTime = data['lastUpdateTime']

chinaTotal = data['chinaTotal']
chinaTotal['累计确诊'] = chinaTotal['confirm']
chinaTotal['现有疑似'] = chinaTotal['suspect']
chinaTotal['累计死亡'] = chinaTotal['dead']
chinaTotal['累计治愈'] = chinaTotal['heal']
chinaTotal['现有确诊'] = chinaTotal['nowConfirm']
chinaTotal['现有重症'] = chinaTotal['nowSevere']
del chinaTotal['confirm']
del chinaTotal['suspect']
del chinaTotal['dead']
del chinaTotal['heal']
del chinaTotal['nowConfirm']
del chinaTotal['nowSevere']

chinaAdd = data['chinaAdd']
chinaAdd['累计确诊新增'] = chinaAdd['confirm']

chinaAdd['现有疑似新增'] = chinaAdd['suspect']
chinaAdd['累计死亡新增'] = chinaAdd['dead']
chinaAdd['累计治愈新增'] = chinaAdd['heal']
chinaAdd['现有确诊新增'] = chinaAdd['nowConfirm']
chinaAdd['现有重症新增'] = chinaAdd['nowSevere']
del chinaAdd['confirm']
del chinaAdd['suspect']
del chinaAdd['dead']
del chinaAdd['heal']
del chinaAdd['nowConfirm']
del chinaAdd['nowSevere']

areaTree = data['areaTree']

china_data = areaTree[0]['children']
china_list = []
for x in range(len(china_data)):
    province = china_data[x]['name']
    province_list = china_data[x]['children']
    for y in range(len(province_list)):
        city = province_list[y]['name']
        total = province_list[y]['total']
        today = province_list[y]['today']
        china_dict = {'province': province, 'city': city, 'total': total, 'today': today}
        china_list.append(china_dict)


# 定义数据处理函数
def name(x):
    name = eval(str(x))['name']
    return name


def confirm(x):
    confirm = eval(str(x))['confirm']
    return confirm


def suspect(x):
    suspect = eval(str(x))['suspect']
    return suspect


def dead(x):
    dead = eval(str(x))['dead']
    return dead


def heal(x):
    heal = eval(str(x))['heal']
    return heal


def deadRate(x):
    deadRate = eval(str(x))['deadRate']
    return deadRate


def healRate(x):
    healRate = eval(str(x))['healRate']
    return healRate


china_data = pd.DataFrame(china_list)
china_data.head()
# 函数映射
china_data['confirm'] = china_data['total'].map(confirm)
china_data['suspect'] = china_data['total'].map(suspect)
china_data['dead'] = china_data['total'].map(dead)
china_data['heal'] = china_data['total'].map(heal)
china_data['deadRate'] = china_data['total'].map(deadRate)
china_data['healRate'] = china_data['total'].map(healRate)
china_data = china_data[
    ["province", "city", "confirm", "suspect", "dead", "heal", "deadRate", "healRate"]]
china_data.head()

g_data = get_global_data()
# # 国际数据处理
global_data = pd.DataFrame(g_data.values())
global_data['name'] = global_data['total'].map(name)
global_data['confirm'] = global_data['total'].map(confirm)
global_data['suspect'] = global_data['total'].map(suspect)
global_data['dead'] = global_data['total'].map(dead)
global_data['heal'] = global_data['total'].map(heal)
global_data['deadRate'] = global_data['total'].map(deadRate)
global_data['healRate'] = global_data['total'].map(healRate)
world_name = pd.read_excel(BASE_DIR + "/spider/files/世界各国中英文对照.xlsx")
global_data = pd.merge(global_data, world_name, left_on="name", right_on="中文", how="inner")
global_data = global_data[
    ["name", "英文", "confirm", "suspect", "dead", "heal", "deadRate", "healRate"]]
global_data.head()

# # 国际数据处理
# global_data = pd.DataFrame(data['areaTree'])
# global_data['confirm'] = global_data['total'].map(confirm)
# global_data['suspect'] = global_data['total'].map(suspect)
# global_data['dead'] = global_data['total'].map(dead)
# global_data['heal'] = global_data['total'].map(heal)
# global_data['deadRate'] = global_data['total'].map(deadRate)
# global_data['healRate'] = global_data['total'].map(healRate)
# world_name = pd.read_excel(BASE_DIR + "/spider/files/世界各国中英文对照.xlsx")
# global_data = pd.merge(global_data, world_name, left_on="name", right_on="中文", how="inner")
# global_data = global_data[
#     ["name", "英文", "confirm", "suspect", "dead", "heal", "deadRate", "healRate"]]
# global_data.head()


# 获得国内疫情历史统计数据
epidemic_data = requests.get('https://file1.dxycdn.com/2020/0330/777/3404904062754687597-135.json?t=26425939').json()

# 日数据处理
for m, v in enumerate(epidemic_data['data']):
    v['dateId'] = str(v['dateId'])[4:6] + '-' + str(v['dateId'])[6:]

chinaDayList = pd.DataFrame(epidemic_data['data'])

chinaDayList = chinaDayList[['dateId', 'confirmedCount', 'suspectedCount', 'deadCount', 'curedCount']]
chinaDayList.head()

# 日新增数据处理
chinaDayAddList = pd.DataFrame(epidemic_data['data'])
chinaDayAddList = chinaDayAddList[['dateId', 'confirmedIncr', 'suspectedCountIncr', 'deadIncr', 'currentConfirmedIncr']]
chinaDayAddList.head()

# 数据可视化

# 饼图
total_pie = (
    Pie(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, bg_color="transparent"))
        .add("", [list(z) for z in zip(chinaTotal.keys(), chinaTotal.values())], center=["50%", "60%"],
             radius=[75, 100])
        .add("", [list(z) for z in zip(chinaAdd.keys(), chinaAdd.values())], center=["50%", "60%"], radius=[0, 50])
        .set_global_opts(
        legend_opts=opts.LegendOpts(type_="scroll", textstyle_opts=opts.TextStyleOpts(color="#FFFFFF")))
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}:{c}")))

# 全球疫情地图
world_map = (
    Map(init_opts=opts.InitOpts(theme=ThemeType.WESTEROS))
        .add("", [list(z) for z in zip(list(global_data["英文"]), list(global_data["confirm"]))], "world",
             is_map_symbol_show=False)
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False),
                         toolbox_opts=opts.ToolboxOpts(orient='vertical', pos_right="10%"))
        .set_global_opts(visualmap_opts=opts.VisualMapOpts(is_piecewise=True, background_color="transparent",
                                                           textstyle_opts=opts.TextStyleOpts(color="#F5FFFA"),
                                                           pieces=[
                                                               {"min": 101, "label": '>100', "color": "#893448"},
                                                               {"min": 10, "max": 100, "label": '10-100',
                                                                "color": "#fb8146"},
                                                               {"min": 1, "max": 9, "label": '1-9',
                                                                "color": "#fff2d1"},
                                                           ])))
# 中国疫情地图绘制
# 数据处理
area_data = china_data.groupby("province")["confirm"].sum().reset_index()

area_data.columns = ["province", "confirm"]

area_map = (
    Map(init_opts=opts.InitOpts(theme=ThemeType.WESTEROS))
        .add("", [list(z) for z in zip(list(area_data["province"]), list(area_data["confirm"]))], "china",
             is_map_symbol_show=False, label_opts=opts.LabelOpts(color="#fff"),
             tooltip_opts=opts.TooltipOpts(is_show=True), zoom=1.2, center=[105, 30])
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(title_opts=opts.TitleOpts(title="中国疫情分布图", pos_top='5%',
                                                   title_textstyle_opts=opts.TextStyleOpts(color="#FF0000")),
                         visualmap_opts=opts.VisualMapOpts(is_piecewise=True, pos_right=0, pos_bottom=0,
                                                           textstyle_opts=opts.TextStyleOpts(color="#F5FFFA"),
                                                           pieces=[
                                                               {"min": 1001, "label": '>1000', "color": "#893448"},
                                                               {"min": 500, "max": 1000, "label": '500-1000',
                                                                "color": "#ff585e"},
                                                               {"min": 101, "max": 499, "label": '101-499',
                                                                "color": "#fb8146"},
                                                               {"min": 10, "max": 100, "label": '10-100',
                                                                "color": "#ffb248"},
                                                               {"min": 0, "max": 9, "label": '0-9',
                                                                "color": "#fff2d1"}])))

city_data = china_data.groupby('city')['confirm'].sum().reset_index()

city_data.columns = ["city", "confirm"]


def is_city(item):
    '''
    判断一个城市能否在Geo地图上被找到
    :param item: 城市名
    :return: T/F
    '''

    lists1 = []
    lists1.append(item)
    lists2 = [10]
    geo = Geo()
    geo.add_schema(maptype="china")
    try:
        geo.add("确诊城市", [list(z) for z in zip(lists1, lists2)])
        return True
    except Exception as e:
        print('异常原因：', e)
        return False


city_index = []
i = 0
for item in city_data['city']:
    if is_city(item) == False:
        city_index.append(i)
    i += 1

for x in city_index:
    del (city_data['city'][x])
    del (city_data['confirm'][x])

city_index_ = []
i = 0
for item in city_data['confirm']:
    if item > 1000:
        city_index_.append(i)
    i += 1

serious_city = []  # 严重城市
serious_submit = []  # 严重人数
for y in city_index_:
    serious_city.append(list(city_data['city'])[y])
    serious_submit.append(list(city_data['confirm'])[y])

list_1 = ["拉萨"]
list_2 = [1]

area_heat_geo = (
    Geo(init_opts=opts.InitOpts(theme=ThemeType.WESTEROS, bg_color='transparent'))
        .add_schema(maptype="china", zoom=1.2, center=[105, 30])
        .add("确诊城市", [list(z) for z in zip(list(city_data["city"]), list(city_data["confirm"]))], symbol_size=10)
        .add("确诊城市", [list(z) for z in zip(list_1, list_2)], symbol_size=10)  # 孤独拉萨
        .add("确诊城市", [list(z) for z in zip(list(serious_city), list(serious_submit))],  # 感染者超1000的城市
             type_=ChartType.EFFECT_SCATTER, effect_opts=opts.EffectOpts(is_show=True, color="black",
                                                                         symbol_size=30, scale=4, period=1))
        .add("", [list(z) for z in zip(list(city_data["city"]), list(city_data["confirm"]))],
             type_=ChartType.HEATMAP)
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
        visualmap_opts=opts.VisualMapOpts(range_size=[0, 25, 50, 75, 100], max_=1000, orient='horizontal',
                                          pos_bottom=0),
        title_opts=opts.TitleOpts(title="中国疫情分布热图", pos_top='5%'),
        legend_opts=opts.LegendOpts(pos_bottom='10%', pos_left=0)))

date = []  # 日期
confirmTotal = []  # 累计确诊
confirmAdd = []  # 新增确诊
suspectTotal = []  # 累计疑似
suspectAdd = []  # 新增疑似
deadTotal = []  # 累计死亡
deadAdd = []  # 新增死亡
healTotal = []  # 累计治愈
healAdd = []  # 新增治愈
deadRate = []  # 死亡率
healRate = []  # 治愈率

for j in epidemic_data['data']:
    confirmAdd.append(j['confirmedIncr'])
    suspectAdd.append(j['suspectedCountIncr'])
    deadAdd.append(j['deadIncr'])
    healAdd.append(j['curedIncr'])

for k in epidemic_data['data']:
    date.append(k['dateId'])
    confirmTotal.append(k['confirmedCount'])
    suspectTotal.append(k['suspectedCount'])
    deadTotal.append(k['deadCount'])
    healTotal.append(k['curedCount'])
    deadRate.append(round((k['deadCount'] / k['confirmedCount']) * 100, 2))
    healRate.append(round((k['curedCount'] / k['confirmedCount']) * 100, 2))

line_1 = (
    Line(init_opts=opts.InitOpts(theme=ThemeType.DARK, bg_color="#333333"))
        .add_xaxis(date)
        .add_yaxis("累计确诊", confirmTotal, yaxis_index=1, is_smooth=True,
                   tooltip_opts=opts.TooltipOpts(formatter="{a}:{c}"))
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter="{value}")),
                         legend_opts=(opts.LegendOpts(textstyle_opts=opts.TextStyleOpts(color="white")))))
bar_1 = (
    Bar(init_opts=opts.InitOpts(theme=ThemeType.DARK, bg_color="#333333"))
        .add_xaxis(date)
        .add_yaxis("单日确诊", confirmAdd)
        .extend_axis(yaxis=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter="{value}")))
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(title_opts=opts.TitleOpts("确诊", pos_left='10%',
                                                   title_textstyle_opts=opts.TextStyleOpts(color="white")),
                         yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter="{value}")),
                         legend_opts=(opts.LegendOpts(textstyle_opts=opts.TextStyleOpts(color="white"))))).overlap(
    line_1)

line_2 = (
    Line(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, bg_color="#333333"))
        .add_xaxis(date)
        .add_yaxis("累计疑似", suspectTotal, yaxis_index=1, is_smooth=True,
                   tooltip_opts=opts.TooltipOpts(formatter="{a}:{c}"))
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter="{value}")),
                         legend_opts=(opts.LegendOpts(textstyle_opts=opts.TextStyleOpts(color="white")))))

bar_2 = (
    Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, bg_color="#333333"))
        .add_xaxis(date)
        .add_yaxis("单日疑似", suspectAdd, tooltip_opts=opts.TooltipOpts(formatter="{a}:{c}"))
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(title_opts=opts.TitleOpts("疑似", pos_left='10%',
                                                   title_textstyle_opts=opts.TextStyleOpts(color="white")),
                         yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter="{value}")),
                         legend_opts=(opts.LegendOpts(textstyle_opts=opts.TextStyleOpts(color="white"))))).overlap(
    line_2)

line_3 = (
    Line(init_opts=opts.InitOpts(theme=ThemeType.DARK, bg_color="#333333"))
        .add_xaxis(date)
        .add_yaxis("累计死亡", deadTotal, yaxis_index=1, is_smooth=True, tooltip_opts=opts.TooltipOpts(formatter="{a}:{c}"))
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter="{value}")),
                         legend_opts=(opts.LegendOpts(textstyle_opts=opts.TextStyleOpts(color="white")))))

bar_3 = (
    Bar(init_opts=opts.InitOpts(theme=ThemeType.DARK, bg_color="#333333"))
        .add_xaxis(date)
        .add_yaxis("单日死亡", deadAdd, tooltip_opts=opts.TooltipOpts(formatter="{a}:{c}"))
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(title_opts=opts.TitleOpts("死亡", pos_left='10%',
                                                   title_textstyle_opts=opts.TextStyleOpts(color="white")),
                         yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter="{value}")),
                         legend_opts=(opts.LegendOpts(textstyle_opts=opts.TextStyleOpts(color="white"))))).overlap(
    line_3)

line_4 = (
    Line(init_opts=opts.InitOpts(theme=ThemeType.ROMA, bg_color="#333333"))
        .add_xaxis(date)
        .add_yaxis("累计治愈", healTotal, yaxis_index=1, is_smooth=True, tooltip_opts=opts.TooltipOpts(formatter="{a}:{c}"))
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter="{value}")),
                         legend_opts=(opts.LegendOpts(textstyle_opts=opts.TextStyleOpts(color="white")))))
bar_4 = (
    Bar(init_opts=opts.InitOpts(theme=ThemeType.ROMA, bg_color="#333333"))
        .add_xaxis(date)
        .add_yaxis("单日治愈", healAdd, tooltip_opts=opts.TooltipOpts(formatter="{a}:{c}"))
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(title_opts=opts.TitleOpts("治愈", pos_left='10%',
                                                   title_textstyle_opts=opts.TextStyleOpts(color="white")),
                         yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter="{value}")),
                         legend_opts=(opts.LegendOpts(textstyle_opts=opts.TextStyleOpts(color="white"))))).overlap(
    line_4)

line = (
    Line(init_opts=opts.InitOpts(theme=ThemeType.CHALK, bg_color="#333333"))
        .add_xaxis(date)
        .add_yaxis("死亡率", deadRate, is_smooth=True, tooltip_opts=opts.TooltipOpts(formatter="{a}:{c}%"))
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(title_opts=opts.TitleOpts("死亡/治愈率", pos_left='10%',
                                                   title_textstyle_opts=opts.TextStyleOpts(color="white")),
                         yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter="{value}")),
                         legend_opts=(opts.LegendOpts(textstyle_opts=opts.TextStyleOpts(color="white")))))

lines = (
    Line(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, bg_color="#333333"))
        .add_xaxis(date)
        .add_yaxis("治愈率", healRate, is_smooth=True, tooltip_opts=opts.TooltipOpts(formatter="{a}:{c}%"))
        .extend_axis(yaxis=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter="{value}%")))
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(title_opts=opts.TitleOpts("死亡/治愈率", pos_left='10%',
                                                   title_textstyle_opts=opts.TextStyleOpts(color="white")),
                         yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter="{value}%")),
                         legend_opts=(opts.LegendOpts(textstyle_opts=opts.TextStyleOpts(color="white"))))).overlap(line)

tojing = (
    Line(init_opts=opts.InitOpts(theme=ThemeType.CHALK, bg_color="transparent"))
        .add_xaxis(list(chinaDayList["dateId"]))
        .add_yaxis("累计确诊               ", list(chinaDayList["confirmedCount"]), is_smooth=True, yaxis_index=1)
        .add_yaxis("累计疑似               ", list(chinaDayList["suspectedCount"]), is_smooth=True, yaxis_index=1)
        .add_yaxis("累计死亡               ", list(chinaDayList["deadCount"]), is_smooth=True, yaxis_index=1)
        .add_yaxis("累计治愈", list(chinaDayList["curedCount"]), is_smooth=True, yaxis_index=1)
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(legend_opts=opts.LegendOpts(pos_left='center')))

tojing_ = (
    Bar(init_opts=opts.InitOpts(theme=ThemeType.CHALK, bg_color="transparent"))
        .add_xaxis(list(chinaDayAddList["dateId"]))
        .add_yaxis("单日确诊               ", list(chinaDayAddList["confirmedIncr"]))
        .add_yaxis("单日疑似               ", list(chinaDayAddList["suspectedCountIncr"]))
        .add_yaxis("单日死亡               ", list(chinaDayAddList["deadIncr"]))
        .add_yaxis("单日治愈", list(chinaDayAddList["currentConfirmedIncr"]))
        .extend_axis(yaxis=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter="{value}")))
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(legend_opts=opts.LegendOpts(pos_left='center'),
                         yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter="{value}")),
                         datazoom_opts=opts.DataZoomOpts())).overlap(tojing)

tl = (
    Timeline(init_opts=opts.InitOpts(theme=ThemeType.WALDEN, bg_color="transparent"))
        .add_schema(play_interval=5000, is_auto_play=True, width='70%', height='10%', pos_left='center',
                    linestyle_opts=opts.LineStyleOpts(), label_opts=opts.LabelOpts(position='bottom', color="white"))
        .add(bar_1, "确诊")
        .add(bar_2, "疑似")
        .add(bar_3, "死亡")
        .add(bar_4, "治愈")
        .add(lines, "死亡/治愈率")
    # .add(tojing, '历史统计')
    # .add(tojing_, '单日统计')

)

big_title = (
    Pie()
        .set_global_opts(
        title_opts=opts.TitleOpts(title="COVID-19",
                                  title_textstyle_opts=opts.TextStyleOpts(font_size=40, color='#FFFFFF',
                                                                          border_radius=True, border_color="white"),
                                  pos_top=0)))

times = (
    Pie()
        .set_global_opts(
        title_opts=opts.TitleOpts(subtitle=("截至 " + lastUpdateTime),
                                  subtitle_textstyle_opts=opts.TextStyleOpts(font_size=13, color='#FFFFFF'),
                                  pos_top=0))
)

confirms = (Pie().
            set_global_opts(title_opts=opts.TitleOpts(title="确诊", pos_left='center', pos_top='center',
                                                      subtitle="(现有)", item_gap=1,
                                                      subtitle_textstyle_opts=opts.TextStyleOpts(color="#FFFFFF"),
                                                      title_textstyle_opts=opts.TextStyleOpts(color='#FFFFFF'))))
confirms_people = (Pie().
                   set_global_opts(title_opts=opts.TitleOpts(title=(str(chinaTotal['现有确诊']) + "   "),
                                                             pos_top='15%', pos_left='center',
                                                             subtitle=("         新增: " + str(chinaAdd['现有确诊新增'])),
                                                             item_gap=1,
                                                             title_textstyle_opts=opts.TextStyleOpts(color="#00FFFF",
                                                                                                     font_size=30),
                                                             subtitle_textstyle_opts=opts.TextStyleOpts(color="#00BFFF")
                                                             )))
suspects = (Pie().
            set_global_opts(title_opts=opts.TitleOpts(title="疑似", pos_left='center', pos_top='center',
                                                      subtitle="(现有)", item_gap=1,
                                                      subtitle_textstyle_opts=opts.TextStyleOpts(color="#FFFFFF"),
                                                      title_textstyle_opts=opts.TextStyleOpts(color='#FFFFFF'))))
suspects_people = (Pie().
                   set_global_opts(title_opts=opts.TitleOpts(title=(str(chinaTotal['现有疑似']) + "   "),
                                                             pos_top='15%', pos_left='center',
                                                             subtitle=("         新增 :" + str(chinaAdd['现有疑似新增'])),
                                                             item_gap=1,
                                                             title_textstyle_opts=opts.TextStyleOpts(color="#FF00FF",
                                                                                                     font_size=30),
                                                             subtitle_textstyle_opts=opts.TextStyleOpts(color="#EE82EE")
                                                             )))
deads = (Pie().
         set_global_opts(title_opts=opts.TitleOpts(title="死亡", pos_left='center', pos_top='center',
                                                   subtitle="(累计)", item_gap=1,
                                                   subtitle_textstyle_opts=opts.TextStyleOpts(color="#FFFFFF"),
                                                   title_textstyle_opts=opts.TextStyleOpts(color='#FFFFFF'))))
deads_people = (Pie().
                set_global_opts(title_opts=opts.TitleOpts(title=(str(chinaTotal['累计死亡']) + "   "),
                                                          pos_top='15%', pos_left='center',
                                                          subtitle=("         新增 :" + str(chinaAdd['累计死亡新增'])),
                                                          item_gap=1,
                                                          title_textstyle_opts=opts.TextStyleOpts(color="#FF0000",
                                                                                                  font_size=30),
                                                          subtitle_textstyle_opts=opts.TextStyleOpts(color="#F08080")
                                                          )))
heals = (Pie().
         set_global_opts(title_opts=opts.TitleOpts(title="治愈", pos_left='center', pos_top='center',
                                                   subtitle="(累计)", item_gap=1,
                                                   subtitle_textstyle_opts=opts.TextStyleOpts(color="#FFFFFF"),
                                                   title_textstyle_opts=opts.TextStyleOpts(color='#FFFFFF'))))
heals_people = (Pie().
                set_global_opts(title_opts=opts.TitleOpts(title=(str(chinaTotal['累计治愈']) + "   "),
                                                          pos_top='15%', pos_left='center',
                                                          subtitle=("         新增 :" + str(chinaAdd['累计治愈新增'])),
                                                          item_gap=1,
                                                          title_textstyle_opts=opts.TextStyleOpts(color="#00FF00",
                                                                                                  font_size=30),
                                                          subtitle_textstyle_opts=opts.TextStyleOpts(color="#98FB98")
                                                          )))

sum = chinaTotal['现有确诊'] + chinaTotal['现有疑似'] + chinaTotal['累计死亡'] + chinaTotal['累计治愈']
confirm_liquid = (
    Liquid()
        .add("确诊比例", [chinaTotal['现有确诊'] / sum], tooltip_opts=opts.TooltipOpts(),
             label_opts=opts.LabelOpts(color="#00FFFF",
                                       font_size=15,
                                       formatter=JsCode(
                                           """function (param) {
                     return (Math.floor(param.value * 10000) / 100) + '%';
                 }"""
                                       ),
                                       position="inside",
                                       ),
             )
)

suspect_liquid = (
    Liquid()
        .add("疑似比例", [chinaTotal['现有疑似'] / sum], tooltip_opts=opts.TooltipOpts(),
             label_opts=opts.LabelOpts(color="#FF00FF",
                                       font_size=15,
                                       formatter=JsCode(
                                           """function (param) {
                     return (Math.floor(param.value * 10000) / 100) + '%';
                 }"""
                                       ),
                                       position="inside",
                                       ),
             )
)

dead_liquid = (
    Liquid()
        .add("死亡比例", [chinaTotal['累计死亡'] / sum], tooltip_opts=opts.TooltipOpts(),
             label_opts=opts.LabelOpts(color="#FF0000",
                                       font_size=15,
                                       formatter=JsCode(
                                           """function (param) {
                     return (Math.floor(param.value * 10000) / 100) + '%';
                 }"""
                                       ),
                                       position="inside",
                                       ),
             )
)

heal_liquid = (
    Liquid()
        .add("治愈比例", [chinaTotal['累计治愈'] / sum], tooltip_opts=opts.TooltipOpts(),
             label_opts=opts.LabelOpts(color="#00FF00",
                                       font_size=15,
                                       formatter=JsCode(
                                           """function (param) {
                     return (Math.floor(param.value * 10000) / 100) + '%';
                 }"""
                                       ),
                                       position="inside",
                                       ),
             )
)

wc = (
    WordCloud()
        .add("", [list(z) for z in zip(list(city_data["city"]), list(city_data["confirm"]))],
             word_gap=0, word_size_range=[10, 30]))

# 图片汇总
# page = (Page(page_title="COVID-19",layout=Page.DraggablePageLayout)
page = (Page(page_title="COVID-19")
        .add(total_pie)
        .add(world_map)
        .add(area_map)
        .add(area_heat_geo)
        # .add(bar)
        .add(tl)
        .add(big_title)
        .add(times)
        .add(confirms)
        .add(confirms_people)
        .add(suspects)
        .add(suspects_people)
        .add(deads)
        .add(deads_people)
        .add(heals)
        .add(heals_people)
        .add(confirm_liquid)
        .add(suspect_liquid)
        .add(dead_liquid)
        .add(heal_liquid)
        .add(wc)
        ).render(BASE_DIR + "/templates/spider/COVID-19 数据一览.html")

with open(BASE_DIR + "/templates/spider/COVID-19 数据一览.html", "r+", encoding='utf-8') as html:
    html_bf = BeautifulSoup(html, 'html.parser')
    divs = html_bf.select('.chart-container')
    divs[0][
        'style'] = "width:411px;height:303px;position:absolute;top:5px;left:0px;border-style:solid;border-color:#444444;border-width:0px;"
    divs[1][
        "style"] = "width:605px;height:274px;position:absolute;top:36px;left:333px;border-style:solid;border-color:#444444;border-width:0px;"
    divs[2][
        "style"] = "width:309px;height:405px;position:absolute;top:313px;left:961px;border-style:solid;border-color:#444444;border-width:0px;"
    divs[3][
        "style"] = "width:305px;height:405px;position:absolute;top:310px;left:0px;border-style:solid;border-color:#444444;border-width:0px;"

    divs[4][
        "style"] = "width:646px;height:304px;position:absolute;top:312px;left:312px;border-style:solid;border-color:#444444;border-width:0px;"
    divs[5][
        "style"] = "width:250px;height:55px;position:absolute;top:2px;left:440px;border-style:solid;border-color:#444444;border-width:0px;"
    divs[6][
        "style"] = "width:200px;height:30px;position:absolute;top:11px;left:675px;border-style:solid;border-color:#444444;border-width:0px;"

    divs[7][
        'style'] = "width:60px;height:75px;position:absolute;top:5px;left:1060px;border-style:solid;border-color:#DC143C;border-width:3px;border-radius:25px 0px 0px 0px"
    divs[8][
        "style"] = "width:130px;height:75px;position:absolute;top:5px;left:1120px;border-style:solid;border-color:#DC143C;border-width:3px;"
    divs[9][
        "style"] = "width:60px;height:75px;position:absolute;top:80px;left:1060px;border-style:solid;border-color:#DC143C;border-width:3px;"
    divs[10][
        "style"] = "width:130px;height:75px;position:absolute;top:80px;left:1120px;border-style:solid;border-color:#DC143C;border-width:3px;"
    divs[11][
        "style"] = "width:60px;height:75px;position:absolute;top:155px;left:1060px;border-style:solid;border-color:#DC143C;border-width:3px;"
    divs[12][
        "style"] = "width:130px;height:75px;position:absolute;top:155px;left:1120px;border-style:solid;border-color:#DC143C;border-width:3px;"
    divs[13][
        "style"] = "width:60px;height:75px;position:absolute;top:230px;left:1060px;border-style:solid;border-color:#DC143C;border-width:3px;"
    divs[14][
        "style"] = "width:130px;height:75px;position:absolute;top:230px;left:1120px;border-style:solid;border-color:#DC143C;border-width:3px;border-radius:0px 0px 25px 0px"

    divs[15][
        "style"] = "width:160px;height:160px;position:absolute;top:-35px;left:920px;border-style:solid;border-color:#444444;border-width:0px;"
    divs[16][
        "style"] = "width:160px;height:160px;position:absolute;top:40px;left:865px;border-style:solid;border-color:#444444;border-width:0px;"
    divs[17][
        "style"] = "width:160px;height:160px;position:absolute;top:115px;left:920px;border-style:solid;border-color:#444444;border-width:0px;"
    divs[18][
        "style"] = "width:160px;height:160px;position:absolute;top:188px;left:865px;border-style:solid;border-color:#444444;border-width:0px;"
    divs[19][
        "style"] = "width:1280px;height:120px;position:absolute;top:600px;left:0px;border-style:solid;border-color:#444444;border-width:0px;"

    body = html_bf.find("body")
    body["style"] = "background-color:#333333;"
    html_new = str(html_bf)
    html.seek(0, 0)
    html.truncate()
    html.write(html_new)
    html.close()

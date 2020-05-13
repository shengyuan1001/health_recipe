import requests
import MySQLdb.cursors

# connect() 方法用于创建数据库的连接，里面可以指定参数：用户名，密码，主机等信息。
# 这只是连接到了数据库，要想操作数据库需要创建游标。
conn = MySQLdb.connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='buzhidao',
    db='hfgdsfwsdsaf',
    charset='utf8',
    cursorclass=MySQLdb.cursors.SSCursor
)

# token = '30ee9721eb9a44df926ea9afb2660fb4'

token = 'b43bfa2d6cb143cf8458f737926b5f3c'
# 执行sql

# 获取查询结果
typeone = {
    '精选': 1,
    '男生': 2,
    '女生': 3,
    'VIP': 4,
    '听书': 5,
}
typechild = {
    '玄幻奇幻': 1,
    '青春爱情': 2,
    '灵异恐怖': 3,
    '名人传记': 4,
    '武侠小说': 5,
    '传统文学': 6,
    '世界名著': 7,
    '红色文化': 8,
    '创业励志': 9,
    '销售职场': 10,
    '投资管理': 11,
    '人生哲学': 12,
    '宗教文化': 13,
    '现代文学': 14,
    '科学幻想': 15,
    '少儿读物': 16,
    '近现代文学。': 14,
    '诺奖全集': 7,
}
status = {
    '已完结': 1,
    '连载中': 0,
}


# sql = "select `id`,`name` from sy_book_category"


def book_sql():
    # 通过获取到的数据库连接conn下的cursor()方法来创建游标。
    cur = conn.cursor()
    sql = "select `id`,`Name`,`Img`,`Author`,`Desc`, `BookStatus`, `LastChapter`,`CId` from sy_book"
    cur.execute(sql)
    results = list(cur.fetchall())
    item = []
    for re in results:
        re = list(re)
        re[5] = status[re[5]]
        re.append(1)
        re.append(1)
        item.append(re)
    cur.close()
    return item


def spider_book(data, url, token):
    item = data
    headers = {
        'AUTHORIZATION': token,
    }
    file = open(item['b_img'], 'rb')
    type_ = 'image/{}'.format(item['b_img'].split('.')[-1])

    files = {
        'b_img': (item['b_img'].split('/')[-1], file, type_)
    }
    # item.pop('id')
    item.pop('b_img')
    while True:
        res = requests.post(url, data=item, files=files, headers=headers)
        print(res.json())
        if res.json()['code'] == 1111:
            continue
        else:
            break


def spider_chapter(data, url, token):
    headers = {
        'AUTHORIZATION': token,
    }
    while True:
        res = requests.post(url, data=data, headers=headers)
        if res.json()['code'] == 1111:
            continue
        else:
            break


def check_book_id(url, token):
    headers = {
        'AUTHORIZATION': token,
    }
    while True:
        res = requests.get(url, headers=headers)
        if res.json()['code'] == 1111:
            continue
        else:
            break
    res_json = res.json()

    if res_json['data']:
        if res_json['data']['results']:
            id = res_json['data']['results'][0]['id']
            return id
    return None


def book_item():
    item = book_sql()
    # with open('txt.txt', 'w')as f:
    #     f.write('sss')
    # with open('public/book/2019/08-01/0a516a250c9106929536ecde81b50557.jpg', 'rb')as f:
    #     file = f.read()
    # print(file)
    body = ['sb', 'b_name', 'b_img', 'b_author', 'b_desc', 'status', 'new_chapter', 'c', 'o', 'index']
    book_list = []
    for i in item:
        img_path = i[2][1:]
        new_img_path = 'img/' + i[1] + '.' + i[2].split('.')[-1]
        i[2] = new_img_path
        # with open(img_path, 'rb')as f:
        #     file = f.read()
        # with open(new_img_path, 'wb')as f:
        #     f.write(file)
        book_list.append(dict(zip(body, i)))
        # print(dict(zip(body, i)))
    return book_list


def chapter_item(item, id):
    body = ['b', 'c_name', 'qq', 'text', 'popo']
    chapter_list = []
    for i in item:
        i = list(i)
        ss = dict(zip(body, i))
        ss['b'] = id
        ss.pop('qq')
        ss.pop('popo')
        chapter_list.append(ss)
    return chapter_list


if __name__ == '__main__':
    book_url = 'http://lddd.whscread.net:8000/novel/whbook/'
    chapter_url = 'http://lddd.whscread.net:8000/novel/chapter/'
    book_list = book_item()
    num = 0
    print(1111111111111111111111)
    cur = conn.cursor()
    sql = "select * from sy_book_chapter"
    cur.execute(sql)
    chapter_list = list(cur.fetchall())
    cur.close()
    print(2222222222222222222222)
    for book in book_list:
        num += 1
        print('第', num, '本')
        if num < 94:
            continue
        # if num < 11:  # 跳过不想要的(默认为4)
        #     continue
        spider_book(book, book_url, token)

        url = book_url + '?b_name={}'.format(book['b_name'])
        id = check_book_id(url, token)
        if id:
            print('sshu数据库中 {} 的 id：{}'.format(book['b_name'], id), '...........', '原数据库书籍id：', book['sb'])
            new_chapter_list = []
            for i in chapter_list:
                i = list(i)
                # print(type(i[2]), i[2], type(book['sb']), book['sb'])
                if int(i[2]) == book['sb']:
                    new_chapter_list.append(i)
            print(len(new_chapter_list))
            data = chapter_item(new_chapter_list, id)
            for i in data:
                spider_chapter(i, chapter_url, token)
    print('完成')

    ''''''

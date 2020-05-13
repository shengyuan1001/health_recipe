import MySQLdb.cursors
import pandas as pd

conn = MySQLdb.connect(
    host='rr-bp1kser46s71ib829uo.mysql.rds.aliyuncs.com',
    port=3306,
    user='ghsjfsdgjhd',
    passwd='sld24gjsigf#hjdflGhj',
    db='hfgdsfwsdsaf',
    charset='utf8',
    cursorclass=MySQLdb.cursors.SSCursor
)


def shiming():
    cur = conn.cursor()
    sql = "SELECT realname,username,mobile,idcard FROM `hfgdsfwsdsaf`.`sy_users` WHERE realname != '' AND is_shiming=1"
    cur.execute(sql)
    user_list = list(cur.fetchall())
    cur.close()
    columns = ['姓名', '手机号', '手机号', '身份证号']
    dt = pd.DataFrame(user_list, columns=columns)
    dt.to_excel('user_shiming_xlsx.xlsx', index=0)
    dt.to_csv('user_shiming_csv.csv')


if __name__ == '__main__':
    shiming()
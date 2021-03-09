import json
import pymysql

def get_filter_hz():
    sum = []
    db = pymysql.connect(host='192.168.2.97', password='BOOT-xwork1024', database='spider', user='root')
    cursor = db.cursor()
    sql = "select company_name,business_project from data_wheel where province_code = 'js' "
    cursor.execute(sql)
    data = cursor.fetchall()
    data = [[i[0], i[1]] for i in data]
    print(data)
    print(len(data))
    # exit()
    for i in data:
        if i[1] == None:
            continue
        if '基础电信业务' in i[1]:
            sum.append(i)
        elif '第一类增值电信业务' in i[1]:
            sum.append(i)
        elif '第二类增值电信业务' in i[1]:
            sum.append(i)
        elif '互联网新闻信息服务' in i[1]:
            sum.append(i)
        elif '药品互联网信息服务' in i[1]:
            sum.append(i)
        elif '互联网信息服务' in i[1]:
            sum.append(i)
        elif '医疗器械互联网信息服务' in i[1]:
            sum.append(i)
        elif '呼叫中心' in i[1]:
            sum.append(i)
        elif '经营电信业务' in i[1]:
            sum.append(i)
    print(len(sum))
    with open(r'D:\projects\Spider\local_spider\Other\spider_all\ICP\data\business_project江苏数据.json', 'a', encoding='utf-8')as fp:
        fp.write(json.dumps(sum, ensure_ascii=False))

get_filter_hz()
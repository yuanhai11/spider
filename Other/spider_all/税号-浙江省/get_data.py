import re
import time
import requests
import pymysql
import json
from sqlalchemy import Column, String, create_engine,Integer
from sqlalchemy.orm import sessionmaker

def get_bloom():
    db = pymysql.connect(host="192.168.2.97", user="root", password='BOOT-xwork1024', database="spider", port=3306)
    cursor = db.cursor()
    sql = "select company_num from company_title"
    cursor.execute(sql)
    db_data = cursor.fetchall()
    data = [i[0] for i in db_data]
    print(data)
    from pybloom_live import ScalableBloomFilter
    bloom = ScalableBloomFilter(initial_capacity=100000, error_rate=0.001)
    for bl in data:
        bloom.add(bl)
    db.close()
    return bloom

def get_data():
    bloom = get_bloom()

    conn = pymysql.connect(host="192.168.2.97", user="root", password='BOOT-xwork1024', database="spider", port=3306)
    cursor = conn.cursor()
    sql = '''SELECT company_num,company_name FROM `company_info` WHERE (`reg_authority` LIKE '建德%' OR `reg_authority` LIKE '绍兴%' OR `reg_authority` LIKE '新昌%' OR `reg_authority`LIKE '诸暨%' OR `reg_authority` LIKE '嵊州%'
        OR `reg_authority` LIKE '金华%' OR `reg_authority` LIKE '武义%' OR `reg_authority` LIKE '浦江%' OR `reg_authority` LIKE '兰溪%' OR `reg_authority` LIKE '义乌%' OR `reg_authority` LIKE '东阳%' OR `reg_authority` LIKE '永康%'
        OR `reg_authority` LIKE '宁波%' OR `reg_authority` LIKE '象山%' OR `reg_authority` LIKE '宁海%' OR `reg_authority` LIKE '余姚%' OR `reg_authority` LIKE '慈溪%')'''
    cursor.execute(sql)
    db_data = cursor.fetchall()

    db_data = [i for i in db_data if i[0] not in bloom]
    with open('data-second.txt','w',encoding='utf-8')as fp:
        fp.write(json.dumps(db_data,ensure_ascii=False))

    cursor.close()
    conn.close()


def load_data():
    with open('data.txt', encoding='utf-8')as fp:
        c = json.loads(fp.read())
    print(len(c))


if __name__ == '__main__':
    # main()
    get_data()
    # load_data()
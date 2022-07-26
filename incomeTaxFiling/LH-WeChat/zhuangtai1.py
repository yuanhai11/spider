# coding: utf-8

#当前脚本修改pc状态为空闲      0

import pymysql
import socket

def get_host_ip():
    sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sk.connect(('114.114.114.114', 80))
    ip_addr = sk.getsockname()[0]
    return ip_addr

def fs(task_id,ip):
    HOST = '192.168.2.99'
    USER = 'root'
    PASSWORD = 'BOOT-xwork1024'
    DATABASE = 'prod_spider'

    conn = pymysql.connect(host='%s' % HOST, user='%s' % USER, password='%s' % PASSWORD, database='%s' % DATABASE,
                           port=3306)
    cursor = conn.cursor()
    sql3 = "update wechat_work_bot set status=1 where bot_ip='{}'".format(ip)
    cursor.execute(sql3)
    sql4 = "delete from wechat_work_task where task_id='{}'".format(task_id)
    cursor.execute(sql4)
    conn.commit()
    conn.close()
    return 'set PC_status=1  task is delete'

# fs()

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
    HOST = 'rm-bp13704xlt13yoe7pvo.mysql.rds.aliyuncs.com'
    USER = 'root'
    PASSWORD = 'BOOT-xwork1024'
    DATABASE = 'spider'

    conn = pymysql.connect(host='%s' % HOST, user='%s' % USER, password='%s' % PASSWORD, database='%s' % DATABASE,
                           port=3306)
    cursor = conn.cursor()
    ip = "192.168.57.141"
    sql3 = "update task_computer set computer_status=1 where computer_ip='{}'".format(ip)
    cursor.execute(sql3)
    # sql4 = "delete from task_company_list where task_id='{}'".format(task_id)
    # cursor.execute(sql4)
    conn.commit()
    conn.close()
    return 'set PC_status=1  task is delete'

fs(1,1)

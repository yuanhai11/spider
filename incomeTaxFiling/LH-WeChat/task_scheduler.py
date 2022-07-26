import random
import time
import pymysql
import requests
import socket
import json

from decouple import config
from db_dbutils_init import logger


class Scheduler(object):

    # 数据库配置信息
    DB_TEST_HOST = config("DB_TEST_HOST")
    DB_TEST_PORT = int(config("DB_TEST_PORT"))
    DB_TEST_DBNAME = config("DB_TEST_DBNAME")
    DB_TEST_USER = config("DB_TEST_USER")
    DB_TEST_PASSWORD = config("DB_TEST_PASSWORD")

    def __init__(self):
        self.logger = logger("task_scheduler")
        self.conn = None
        self.cursor = None

    def get_conn(self):
        self.conn = pymysql.connect(host='%s' % self.DB_TEST_HOST, user='%s' % self.DB_TEST_USER,
                                    password='%s' % self.DB_TEST_PASSWORD, database='%s' % self.DB_TEST_DBNAME,
                                    port=self.DB_TEST_PORT)
        self.cursor = self.conn.cursor()

    def get_host_ip(self):
        sk = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        sk.connect(('114.114.114.114',80))
        ip_addr = sk.getsockname()[0]
        return ip_addr

    def execute_task(self):
        self.get_conn()
        self.logger.info("""<==== task_scheduler 用于分配任务 循环查询数据库  一旦条件符合 发送请求给客户端  客户端再执行程序 ====>""")
        while 1:
            time.sleep(1)
            try:

                sql = "select bot_id from wechat_work_task group by bot_id"

                self.cursor.execute(sql)  # 执行sql
                self.conn.commit()

                all_bot = self.cursor.fetchall()
                for b in all_bot:

                    sql = "select bot_id,bot_ip from wechat_work_bot where bot_id='{}' and status=1".format(b[0])
                    self.cursor.execute(sql)  # 执行sql
                    self.conn.commit()


                    bot = self.cursor.fetchone()

                    if not bot:
                        continue

                    bot_id = bot[0]
                    ip = bot[1]

                    sql = "select task_id,task_type,bot_id,request_params from wechat_work_task where bot_id='{}' and status=1".format(bot_id)
                    self.cursor.execute(sql)  # 执行sql
                    self.conn.commit()
                    task = self.cursor.fetchone()

                    if not task:
                        continue

                    task_id = task[0]
                    task_type = task[1]
                    content = eval(task[3].replace('"',''))

                    self.logger.info('staring -----')
                    try:
                        xnj_url = 'http://%s:4444' % ip
                        data = {
                                'task_id': '%s' % task_id,'task_type': '%s' % task_type,
                                'bot_id': '%s' % bot_id,'content': "-".join(content)
                                }
                        data = json.dumps(data).encode('utf-8')
                        response = requests.request("POST", xnj_url, data=data).text.encode('latin-1').decode('utf8')
                        self.logger.info('====> bot执行中，task_id:{}--bot_id:{}--computer_ip:{}'.format(task_id,bot_id,ip))
                    except Exception as e:
                        self.logger.error(e)
                        self.logger.error("====> 电脑联系不上，可能出现故障，bot_status=2,computer_ip:{}".format(bot[1]))
                        sql2 = "update wechat_work_bot set status =2,is_shutdown=1 where bot_ip='{}'" \
                            .format(ip)
                        self.cursor.execute(sql2)
                        self.conn.commit()
                          # 直接callback错误信息
                        headers2 = {
                            'Content-Type': 'application/json;charset=UTF-8',
                            'Host': '47.99.96.186:38059'
                        }
                        if not task_id:
                            task_id = 0

                        data = {
                            "taskId": int(task_id),
                            "status": 70017,
                            "msg": '{}'.format(e)
                        }
                        data = json.dumps(data)
                        aaa = requests.post(url='http://47.99.96.186:38059/api/wechat/callback', data=data, headers=headers2).text


            except Exception as out_e:
                self.logger.error('====> 其他错误1.数据库连接异常 2.未知错误：{}'.format(out_e))
                out_e = str(out_e)
                if 'MySQL server' in out_e:
                    self.get_conn()



if __name__ == '__main__':

    schedule = Scheduler()
    schedule.execute_task()
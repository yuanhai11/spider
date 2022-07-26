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
        self.logger.info("""task_scheduler 用于分配任务 循环查询数据库  一旦条件符合 发送请求给客户端  客户端再执行程序""")
        while 1:
            time.sleep(1)
            try:
                sql = "select city from task_company_list group by city "
                self.cursor.execute(sql)  # 执行sql
                self.conn.commit()
                # # 查询所有数据，返回结果默认以元组形式，所以可以进行迭代处理
                citys = self.cursor.fetchmany(200)

                for city in citys:
                    sql1 = "select task_id,content from task_company_list where city='{}' and status = 1".format(city[0])
                    self.cursor.execute(sql1)  # 执行sql
                    self.conn.commit()

                    all_content = self.cursor.fetchone()
                    if not all_content:
                        # print('报税数据已经为零,或没有状态为1的')
                        continue
                    else:
                        task_id = all_content[0]
                        content = all_content[1]
                    sql2 = "select computer_ip from task_computer where computer_city='{}' and computer_status=1".format(
                        city[0])
                    self.cursor.execute(sql2)
                    self.conn.commit()

                    hosts = self.cursor.fetchmany(200)
                    for h in hosts:
                        self.logger.info('staring -----')
                        try:
                            # 发送报税请求给虚拟机
                            xnj_url = 'http://%s:3333' % h[0]
                            data = {'task_id': '%s' % task_id, 'city': '%s' % city[0], 'content': '%s' % content}
                            data = json.dumps(data).encode('utf-8')
                            response = requests.request("POST", xnj_url, data=data).text.encode('latin-1').decode('utf8')
                            self.logger.info('over ------  task_id:{}----computer_ip:{}'.format(task_id, h[0]))
                            break
                        except Exception as e:
                            self.logger.error(e)
                            self.logger.error("电脑联系不上，可能出现故障，status=2,computer:{}".format(h[0]))
                            sql2 = "update task_computer set computer_status =2 where computer_ip='{}'"\
                                .format(h[0])
                            self.cursor.execute(sql2)
                            self.conn.commit()


            except Exception as out_e:
                self.logger.error('任务调度最外层异常捕获：{}'.format(out_e))
                out_e = str(out_e)
                if 'MySQL server' in out_e:
                    self.get_conn()



if __name__ == '__main__':

    schedule = Scheduler()
    schedule.execute_task()
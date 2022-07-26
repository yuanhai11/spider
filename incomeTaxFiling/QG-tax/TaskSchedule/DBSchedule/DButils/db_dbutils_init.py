import pymysql
import logging

from dbutils.pooled_db import PooledDB
from decouple import config
from kafka import KafkaConsumer

"""
@功能：创建数据库连接池
"""

class MyConnectionPool(object):
    DB_TEST_HOST = config("DB_TEST_HOST")
    DB_TEST_PORT = int(config("DB_TEST_PORT"))
    DB_TEST_DBNAME = config("DB_TEST_DBNAME")
    DB_TEST_USER = config("DB_TEST_USER")
    DB_TEST_PASSWORD = config("DB_TEST_PASSWORD")

    DB_MIN_CACHED = int(config("DB_MIN_CACHED"))
    DB_MAX_CACHED = int(config("DB_MAX_CACHED"))
    DB_MAX_SHARED = int(config("DB_MAX_SHARED"))
    DB_MAX_CONNECTIONS = int(config("DB_MAX_CONNECTIONS"))
    DB_MAX_USAGE = int(config("DB_MAX_USAGE"))

    # 单例
    __pool = None
    
    # def __init__(self):
    #     self.conn = self.__getConn()
    #     self.cursor = self.conn.cursor()

    # 创建数据库连接conn和游标cursor
    # def __enter__(self):
    #     self.conn = self.__getconn()
    #     self.cursor = self.conn.cursor()

    # 创建数据库连接池
    def __getconn(self):
        if self.__pool is None:
            self.__pool = PooledDB(
                creator= pymysql,
                mincached=self.DB_MIN_CACHED,
                maxcached=self.DB_MAX_CACHED,
                maxshared=self.DB_MAX_SHARED,
                maxconnections=self.DB_MAX_CONNECTIONS,
                blocking=True,
                maxusage=self.DB_MAX_USAGE,
                setsession=None,
                host=self.DB_TEST_HOST,
                port=self.DB_TEST_PORT,
                user=self.DB_TEST_USER,
                passwd=self.DB_TEST_PASSWORD,
                db=self.DB_TEST_DBNAME,
                use_unicode=False,
                charset='utf8',

            )
        return self.__pool.connection()

    # 释放连接池资源
    # def __exit__(self, exc_type, exc_val, exc_tb):
    #     self.cursor.close()
    #     self.conn.close()

    # 从连接池中取出一个连接
    def getconn(self):
        conn = self.__getconn()
        cursor = conn.cursor()
        return cursor, conn


class MyKafkaConsumer(object):

    PTAX_ZERO_DECLARE = config('PTAX_ZERO_DECLARE')
    BOOTSTRAP_SERVERS = config('BOOTSTRAP_SERVERS').split(',')
    GROUP_ID = config('GROUP_ID')
    AUTO_OFFSET_RESET = config('AUTO_OFFSET_RESET')
    ENABLE_AUTO_COMMIT = eval(config('ENABLE_AUTO_COMMIT'))
    CONSUMER_TIMEOUT_MS = eval(config('CONSUMER_TIMEOUT_MS'))

    def __get_kafka_consumer(self):

        consumer = KafkaConsumer(
            self.PTAX_ZERO_DECLARE,
            bootstrap_servers=self.BOOTSTRAP_SERVERS,
            group_id=self.GROUP_ID,
            auto_offset_reset=self.AUTO_OFFSET_RESET,
            enable_auto_commit=self.ENABLE_AUTO_COMMIT,
            consumer_timeout_ms=self.CONSUMER_TIMEOUT_MS,
            # max_poll_interval_ms=50 * 60 * 1000,
            # max_poll_records=100
            # session_timeout_ms=self.,

        )
        return consumer

    def get_kafka_consumer(self):

        return self.__get_kafka_consumer()



# 获取连接池,实例化
def get_my_connection():
    return MyConnectionPool()

def get_my_kafka_consumer():
    return MyKafkaConsumer()

def logger(log):
    # logger配置信息
    logger = logging.getLogger(log)
    # 指定logger输出格式
    formatter = logging.Formatter(
        '%(asctime)s [%(module)s] [%(threadName)s] %(levelname)5s [%(funcName)s] - %(message)s')
    # 文件日志
    file_handler = logging.FileHandler("./log/{}.log".format(log))
    file_handler.setFormatter(formatter)  # 可以通过setFormatter指定输出格式
    # 控制台日志
    console_handler = logging.StreamHandler()
    console_handler.formatter = formatter  # 也可以直接给formatter赋值
    # 为logger添加的日志处理器，可以自定义日志处理器让其输出到其他地方
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    # 指定日志的最低输出级别，默认为WARN级别
    logger.setLevel(logging.INFO)
    return logger


if __name__ == '__main__':
    cursor,conn = MyConnectionPool().getconn()
    print(cursor,conn)
    pass
    kafka = MyKafkaConsumer()
    logger('1')


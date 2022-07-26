import json
import time

from kafka import KafkaConsumer

from db_dbutils_init import get_my_connection
from db_dbutils_init import get_my_kafka_consumer
from db_dbutils_init import logger

"""执行语句查询有结果返回结果没有返回0；增/删/改返回变更数据条数，没有返回0"""


class MySqLHelper(object):
    def __init__(self):
        self.db = get_my_connection()  # 从数据池中获取连接
        self.consumer = get_my_kafka_consumer().get_kafka_consumer()
        self.logger = logger("task_receive")

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'inst'):  # 单例
            cls.inst = super(MySqLHelper, cls).__new__(cls, *args, **kwargs)
        return cls.inst

    # 封装执行命令
    def my_execute(self, sql, autoclose=False):
        """
        【主要判断是否有参数和是否执行完就释放连接】
        :param sql: 字符串类型，sql语句
        :param param: sql语句中要替换的参数"select %s from tab where id=%s" 其中的%s就是参数
        :param autoclose: 是否关闭连接
        :return: 返回连接conn和游标cursor
        """
        cursor, conn = self.db.getconn()  # 从连接池获取连接
        count = 0
        count = cursor.execute(sql)
        conn.commit()
        self.logger.info("数据插入成功！")

        if autoclose:
            self.close(cursor, conn)

        return cursor,conn,count

    # 释放连接
    def close(self, cursor, conn):
        """释放连接归还给连接池"""
        cursor.close()
        conn.close()


    def insert(self):

        try:
            message = next(self.consumer)
            message_dict = json.loads(message.value.decode("utf-8"))
            self.logger.info(message_dict)
            task_id = message_dict['taskId']
            bot_id = message_dict['botId']
            task_type = message_dict['taskType']
            content = message_dict.get("requestParams")
            sql1 = 'insert into wechat_work_task (id,task_id,task_type,request_params,bot_id,status) values' \
                   ' (NULL ,"%s","%s","%s","%s","%s")' % \
                   (task_id, task_type,str(content),bot_id,1)

            self.my_execute(sql=sql1, autoclose=True)

            self.consumer.commit()

        except StopIteration:
            time.sleep(1)

        except Exception as e:
            self.logger.error(e)



if __name__ == '__main__':
    db = MySqLHelper()

    while 1:
        db.insert()

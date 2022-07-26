from kafka import KafkaConsumer
import time
import pymysql
import logging
import json

logger = logging.getLogger("task_receive")
# 指定logger输出格式
formatter = logging.Formatter('%(asctime)s [%(module)s] [%(threadName)s] %(levelname)5s [%(funcName)s] - %(message)s')
# 文件日志
file_handler = logging.FileHandler("..log/task_receive.log")
file_handler.setFormatter(formatter)  # 可以通过setFormatter指定输出格式
# 控制台日志
console_handler = logging.StreamHandler()
console_handler.formatter = formatter  # 也可以直接给formatter赋值
# 为logger添加的日志处理器，可以自定义日志处理器让其输出到其他地方
logger.addHandler(file_handler)
logger.addHandler(console_handler)
# 指定日志的最低输出级别，默认为WARN级别
logger.setLevel(logging.INFO)

# 数据库配置信息
HOST='192.168.2.99'
USER='root'
PASSWORD='BOOT-xwork1024'
DATABASE='prod_spider'

consumer = KafkaConsumer(
    'ptax_zero_declare',
    bootstrap_servers=['47.99.106.174:9091','47.99.106.174:9092','47.99.106.174:9093'],
    group_id='group-1',
    auto_offset_reset='earliest',
    enable_auto_commit=False,
    consumer_timeout_ms=3 * 1000,
    # max_poll_interval_ms=50 * 60 * 1000,
    # max_poll_records=100
    # session_timeout_ms=,

)
conn = pymysql.connect(host='%s' % HOST, user='%s' % USER, password='%s' % PASSWORD, database='%s' % DATABASE,
                       port=3306)
cursor = conn.cursor()
logger.info('开始接受kafka消息！！！')

while True:

    try:
        message = next(consumer)
        message_dict = json.loads(json.loads(message.value.decode("utf-8")))
        logger.info(message_dict)
        task_id = message_dict['taskId']
        city = message_dict['orgName']
        content = str(message_dict['requestParams'])
        times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        sql1 = 'insert into task_company_list (id,task_id,city,status,content,gmt_created,gmt_updated) values (NULL ,"%s","%s","%s","%s","%s","%s")'%(task_id,city,1,content,times,times)

        cursor.execute(sql1)  # 执行sql
        conn.commit()
        consumer.commit()
        time.sleep(0.2)
    except StopIteration:
        time.sleep(1)
    except Exception as e:
        logger.error('出现异常--{}'.format(e))
        e = str(e)
        if 'MySQL server' in e:
            conn = pymysql.connect(host='%s' % HOST, user='%s' % USER, password='%s' % PASSWORD, database='%s' % DATABASE,port=3306)
            cursor = conn.cursor()
            sql2 = 'insert into task_company_list (id,task_id,city,status,content,gmt_created,gmt_updated) values (NULL ,"%s","%s","%s","%s","%s","%s")' % (
            task_id, city, 1, content, times, times)
            cursor.execute(sql2)  # 执行sql
            conn.commit()
            logger.error('重新链接mysql并提交成功'.format(e))
            consumer.commit()

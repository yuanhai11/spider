import time
import pymysql
import requests
import socket
import logging
# SERVER_ADDR_ONE = config('SERVER_ADDR_ONE')
# SERVER_ADDR_TWO = config('SERVER_ADDR_TWO')
# SERVER_ADDR_THREE = config('SERVER_ADDR_THREE')
# SERVER_ADDR_FOUR = config('SERVER_ADDR_FOUR')
# SERVER_ADDR_FIVE = config('SERVER_ADDR_FIVE')

# 数据库配置信息
HOST='192.168.2.99'
USER='root'
PASSWORD='BOOT-xwork1024'
DATABASE='prod_spider'

# logger配置信息
logger = logging.getLogger("task_scheduler")
# 指定logger输出格式
formatter = logging.Formatter('%(asctime)s [%(module)s] [%(threadName)s] %(levelname)5s [%(funcName)s] - %(message)s')
# 文件日志
file_handler = logging.FileHandler("../log/task_scheduler.log")
file_handler.setFormatter(formatter)  # 可以通过setFormatter指定输出格式
# 控制台日志
console_handler = logging.StreamHandler()
console_handler.formatter = formatter  # 也可以直接给formatter赋值
# 为logger添加的日志处理器，可以自定义日志处理器让其输出到其他地方
logger.addHandler(file_handler)
logger.addHandler(console_handler)
# 指定日志的最低输出级别，默认为WARN级别
logger.setLevel(logging.INFO)

logger.info("""task_scheduler 用于分配任务 循环查询数据库  一旦条件符合 发送请求给客户端  客户端再执行程序""")
def get_host_ip():
    sk = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sk.connect(('114.114.114.114',80))
    ip_addr = sk.getsockname()[0]
    return ip_addr

#设置ip对应的公司id区间    负载均衡的策略 根据 range(0,2) 找到对象的 执行的电脑
# if DEBUG:
#     local_ip = get_host_ip()
#     ll = {'%s' % local_ip: range(0, 10)}
# else:
#     ll = {'%s'%SERVER_ADDR_ONE:range(0,2),'%s'%SERVER_ADDR_TWO:range(2,4),'%s'%SERVER_ADDR_THREE:range(4,6),'%s'%SERVER_ADDR_FOUR:range(6,8),'%s'%SERVER_ADDR_FIVE:range(8,10)}

# master_url = "http://127.0.0.1:2229"
conn = pymysql.connect(host='%s' % HOST, user='%s' % USER, password='%s' % PASSWORD, database='%s' % DATABASE,
               port=3306)
cursor = conn.cursor()

while 1:
    time.sleep(1)
    try:

        sql = "select city from task_company_list group by city "
        cursor.execute(sql)  # 执行sql
        conn.commit()
        # # 查询所有数据，返回结果默认以元组形式，所以可以进行迭代处理
        citys = cursor.fetchmany(200)

        for city in citys:
            sql1 = "select task_id,content from task_company_list where city='{}' and status = 1".format(city[0])
            cursor.execute(sql1)  # 执行sql
            conn.commit()

            all_content = cursor.fetchone()
            if not all_content:
                # print('报税数据已经为零,或没有状态为1的')
                continue
            else:
                task_id = all_content[0]
                content = all_content[1]
            sql2 = "select computer_ip from task_computer where computer_city='{}' and computer_status=1".format(city[0])
            cursor.execute(sql2)
            conn.commit()

            hosts = cursor.fetchmany(200)
            for h in hosts:
                logger.info('staring -----')
                try:
                    #发送报税请求给虚拟机
                    xnj_url = 'http://%s:3333'%h[0]
                    data = {'task_id':'%s'%task_id,'city':'%s'%city[0],'content':'%s'%content}
                    import json
                    data = json.dumps(data).encode('utf-8')
                    response = requests.request("POST", xnj_url, data=data).text.encode('latin-1').decode('utf8')
                    logger.info('over ------  task_id:{}----computer_ip:{}'.format(task_id,h[0]))
                    break
                except Exception as e:
                    logger.info(e)

    except Exception as out_e:
        logger.info('任务调度最外层异常捕获：{}'.format(out_e))
        out_e = str(out_e)
        if 'MySQL server' in out_e:
            conn = pymysql.connect(host='%s' % HOST, user='%s' % USER, password='%s' % PASSWORD, database='%s' % DATABASE,
                                   port=3306)
            cursor = conn.cursor()

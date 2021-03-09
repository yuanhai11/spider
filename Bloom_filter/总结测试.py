import pymysql
import time
'''
列表推导式比循环要快许多（50%左右）但是时间复杂度一样的
'''
# conn = pymysql.connect(port=3306,host='192.168.2.222',user='root',password='123456',database='test')
# cursor = conn.cursor()
# sql = "select * from qcc_source_data"
# cursor.execute(sql)
# data = cursor.fetchall()
#
# data = [i[2] for i in data]*10
# print(data)
# print(len(data))
# a = []
# t1 = time.time()
# for i in data:
#     if 'www.qcc.com' in i:
#         a.append(i)
# t2 = time.time()
# tt = t2-t1
#
# t1 = time.time()
# a = [i for i in data if 'www.qcc.com' in i]
# t2 = time.time()
# ttttt = t2-t1
#
# print(ttttt/tt)

'''
布隆多滤器的实现与原理：
布隆过滤器只能告诉我们：这个值一定不存在或可能存在
    1、布隆过滤器内部有个位数组，具有一定的长度，
    2、含有 多个 hash函数（对每次的值进行哈希），哈希的值对应的位置上标为1，
    3、下次对值进行哈希时，如果 多 个位上有一个不为1，判定一定不存在。如果都为1，判定可能存在（可能key值碰撞的问题）
优点：
    高效的插入和查询    
核心思想：
    1、多个hash函数对目标进行hash，尽可能的减少碰撞（巧合）几率
    2、扩大数组的范围，尽可能的减少碰撞（巧合）几率
    3、ScalableBloomFilter（可以扩容）、BloomFilter（定长的）
    4、不确定长度情景使用ScalableBloomFilter、否则使用BloomFilter
    5、参数capacity：初始化容量；大会浪费内存，小会影响准确率
       参数error_rate：容错率：越小需要内存空间越大，
        需要合理化两个参数的值
应用：
    1、缓存击穿问题：
        - 一般是查询缓存，没有的话查询数据库，数据库没有的话，每次查询都请求数据库，结果给数据库造成巨大压力；
        - 把数据库中的key放在布隆过滤器中，请求后先查询过滤器，过滤器没有直接返回；存在再查询数据库。
    2、黑名单校验
        - 黑名单（垃圾邮件-量级：数以万亿）耗费存储空间，将黑名单放入过滤器里，直接插过滤器即可。
    3、爬虫url去重
'''
from pybloom_live import ScalableBloomFilter,BloomFilter
bloom = ScalableBloomFilter(initial_capacity=100,error_rate=0.001)
url1 = ['http://www.baidu.com','http://www.sssssss.com']
url2 = 'http://www.xina.com'
url3 = 'http://www.xina.com'

bloom.add(url2)
print(len(bloom))
bloom.add(url3)
print(len(bloom))


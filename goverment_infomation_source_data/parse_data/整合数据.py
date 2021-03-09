import requests
import pymysql
'''
将各个网站中的数据规整在一张表中
'''
db = pymysql.connect(host="localhost", user="root", password='123456', database="spider_gaoxinqiye", port=3306)
cursor = db.cursor()
sql = 'show tables'
cursor.execute(sql)

data = cursor.fetchall()
print(data)
print(len(data))


one = []
two = []
three = []
four = []
five = []
six = []
seven = []
eight = []
nine = []
ten = []
for i in data:
    if 'one' in i[0]:
        one.append(i[0])
    elif 'two' in i[0]:
        two.append(i[0])
    elif 'three' in i[0]:
        three.append(i[0])
    elif 'four' in i[0]:
        four.append(i[0])
    elif 'five' in i[0]:
        five.append(i[0])
    elif 'six' in i[0]:
        six.append(i[0])
    elif 'seven' in i[0]:
        seven.append(i[0])
    elif 'eight' in i[0]:
        eight.append(i[0])
    elif 'nine' in i[0]:
        nine.append(i[0])
    elif 'ten' in i[0]:
        ten.append(i[0])

print(one)
print(two)
print(three)
print(four)
print(five)
print(six)
print(seven)
print(eight)
print(nine)
print(ten)

all = []
def get_data(sum):
    for i in sum:
        sql = 'select * from {}'.format(i)
        cursor.execute(sql)
        data = cursor.fetchall()
        print(data)
        for j in data:
            all.append(j)

get_data(one)
get_data(two)
get_data(three)
get_data(four)
get_data(five)
get_data(six)
get_data(seven)
get_data(eight)
get_data(nine)
get_data(ten)

for j in all:
    url = j[1]
    title = j[2]
    gmt_updated = j[4]
    project_name = j[3]
    source = j[5]
    area = j[6]
    sql = """insert into spider_a_data (id,url,title,project_name,gmt_updated,source,area)values(NULL,'{}','{}','{}','{}','{}','{}')""".format(url,title,project_name,gmt_updated,source,area)
    cursor.execute(sql)

db.commit()
db.close()


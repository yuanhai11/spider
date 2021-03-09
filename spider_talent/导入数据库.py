import pymysql,json

db = pymysql.connect(host="localhost",user="root",password='123456',database="test",port=3306)
cursor = db.cursor()
with open('word文档/all_outstanding Tanlent.json', 'r', encoding='utf8')as f:
    content = json.loads(f.read()).get('outstanding_tanlent')

for i in content:
    n = i.get('name')
    company = i.get('company')
    area = i.get('area')

    sql = """insert into outstandingtalent (id,name,companyname,area)values(NULL,'{}','{}','{}')""".format(n,company,area)
    cursor.execute(sql)
    db.commit()
db.close()
    # exit()




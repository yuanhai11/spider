import pymysql

db = pymysql.connect(host='192.168.2.99',password='BOOT-xwork1024',database='spider',user='root')
cursor = db.cursor()

sql = ''

# cursor.execute(sql)
# db.commit()
# db.close()

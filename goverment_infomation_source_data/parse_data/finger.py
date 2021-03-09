import pymysql
import hashlib

m = hashlib.md5()
db = pymysql.connect(host="localhost", user="root", password='123456', database="spider_gaoxinqiye", port=3306)
cursor = db.cursor()
def main():

    sql = 'select * from spider_all_data'
    cursor.execute(sql)
    data = cursor.fetchall()
    print(data)
    # for i in data:
    #     print(i[8])
    # exit()
    for i in data:
        result = hashlib.md5(i[1].encode(encoding='utf-8')).hexdigest()
        print(result)
    # exit()

if __name__ == '__main__':

    exit()
    main()

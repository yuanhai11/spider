import pymysql
conn = pymysql.connect(host='192.168.2.222', user='root', password='123456', database='test', port=3306)
cursor = conn.cursor()

def get_data(sql):
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

def insert_db(data):
    for i in data:
        park_name = i[1]
        park_id = i[2]
        province = i[3]
        city = i[4]
        area = i[5]
        gmt_created = i[6]
        gmt_updated = i[7]

        sql = """insert into qcc_source_data (id,park_name,park_id,province,city,area,gmt_created,gmt_updated)values(NULL,'{}','{}','{}','{}','{}','{}','{}')""".format(park_name,park_id,province,city,area,gmt_created,gmt_updated)
        cursor.execute(sql)
    conn.commit()
    conn.close()

def main():

    sql = "SELECT * FROM qcc_source_data"
    result = get_data(sql)
    data = [i[1] for i in result]
    a = set(data)

    sql1 = "SELECT * FROM tyc_source_data"
    result1 = get_data(sql1)
    data1 = [i[1] for i in result1]
    b = set(data1)

    c = a&b
    new_data = b-c
    print(new_data)
    print('天眼查独有的数据为：',new_data)

    data = [i for i in result1 for j in new_data if i[1]==j]
    print(data)

    if len(data)!=0:
        insert_db(data)
    else:
        print('天眼查  不含  企查查没有的数据！！！')
if __name__ == '__main__':
    main()
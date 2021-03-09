import pymysql
'''
解析2019和2017的docx，docx转为csv进行入库
'''
def insert_db(sum):
    db = pymysql.connect(host="localhost", user="root", password='123456', database="spider_gaoxinqiye", port=3306)
    cursor = db.cursor()
    for i in sum:
        company_name = i[1]
        company_place = i[0]
        get_honor_year = '2019'
        type_of_honor = '省科技型中小'
        batch = ''
        sql = """insert into spider_shengkejixingzhongxiaoqiye_company (id,company_name,company_place,get_honor_year,types_of_honor,batch)
                values(NULL,'{}','{}','{}','{}','{}')""".format(company_name,company_place,get_honor_year,type_of_honor,batch)
        cursor.execute(sql)
        db.commit()
    db.close()
def main():
    xixi = ""
    flag = True
    sum = []
    with open('../2017.csv', encoding='gbk')as fp:
        content = fp.readlines()

    for i in content:
        i = i.replace(',','').replace('2.02E+13','').strip()
        # print(i)
        if i=='':
            flag = False
            xixi = '浙江'
            continue

        if '家）' in i and flag:
            xixi = i.split('（')[0]

        name = i
        if '家）'  in i:
            name =  i.split('家）')[-1]

        area = xixi
        print((area,name))
        sum.append((area,name))
    print(len(sum))
    insert_db(sum)
if __name__ == '__main__':
    main()


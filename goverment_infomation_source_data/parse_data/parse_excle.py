from xlrd import open_workbook
import pymysql

def insert_db(sum):
    db = pymysql.connect(host="localhost", user="root", password='123456', database="spider_gaoxinqiye", port=3306)
    cursor = db.cursor()
    for i in sum:
        company_name = i[0]
        company_place = i[1]
        get_honor_year = i[2]
        type_of_honor = i[3]
        batch = ''

        sql = """insert into company_honor (id,company_name,company_place,get_honor_year,types_of_honor,batch)
                values(NULL,'{}','{}','{}','{}','{}')""".format(company_name,company_place,get_honor_year,type_of_honor,batch)
        cursor.execute(sql)
        db.commit()
    db.close()

def main():
    workbook = open_workbook(r'C:\Users\20945\Desktop\Spider\now_spider\goverment_infomation_source_data\files\附件2-高新区2010-2018年认定的市级科技型初创企业培育工程企业（雏鹰、青蓝）名单 (1).xls')  # 打开excel文件
    sheet2 = workbook.sheet_by_index(0)

    print(sheet2.nrows)
    sum = []
    for i in range(1,sheet2.nrows):
        name = sheet2.cell(i,1).value
        area = sheet2.cell(i,2).value
        year = sheet2.cell(i,3).value
        type = sheet2.cell(i,4).value
        print((name,area,int(year),type))
        sum.append((name,area,int(year),type))
    insert_db(sum)
if __name__ == '__main__':
    main()
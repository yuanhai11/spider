from sqlalchemy import Column, String, create_engine,Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# 创建对象的基类:
Base = declarative_base()
# 定义User对象:

class Medicine(Base):
    # 表的名字:
    __tablename__ = 'spider_abnormal'
    id = Column(Integer(), primary_key=True,autoincrement=True)
    company_name = Column(String(256))
    abnormal_date = Column(String(256))
    area = Column(Integer())
    company_id = Column(String(256))

# 初始化数据库连接:
engine = create_engine('mysql+pymysql://root:BOOT-xwork1024@192.168.2.97:3306/spider')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
# 创建session对象:
session = DBSession()


def parse_excle():
    from xlrd import open_workbook
    import os
    area = '龙泉市'
    data = os.listdir(r'D:\projects\Spider\local_spider\Other\spider_all\Certificate\税务非正常户\{}'.format(area))
    # data = [1]
    # data = ['国家税务总局建德市税务局2019年7月非正常户公示.xlsx']
    for index,d in enumerate(data):
        # if index < 10:
        #     continue
        # if '.docx'  in d:
        #     continue
        # if index==1 or index ==3 or index==5:
        #     continue
        import re
        month = re.findall(r'国家税务总局龙泉市税务局非正常户认定信息公示（2019年(.*?)月1日-2019.*?）',d)[0]
        '''
        
        if ddd == '一':
            ddd = '01'
        elif ddd == '二':
            ddd = '02'
        elif ddd == '三':
            ddd = '03'
        elif ddd == '四':
            ddd = '04'
        elif ddd == '五':
            ddd = '05'
        elif ddd == '六':
            ddd = '06'
        elif ddd == '七':
            ddd = '07'
        elif ddd == '八':
            ddd = '08'
        elif ddd == '九':
            ddd = '09'
        elif ddd == '十一':
            ddd = '11'
        # print(ddd)
        '''

        # year = ddd[0][0]
        # month = ddd[0][1]
        # month = str(int(month) - 1)
        # if month == '0':
        #     year = str(int(year) - 1)
        #     month = '12'

        if len(month) == 1:
            month = '0' + month
        date = '2019' + month

        path = os.path.join(r'D:\projects\Spider\local_spider\Other\spider_all\Certificate\税务非正常户\{}'.format(area),d)
        # path = os.path.join('D:\projects\Spider\local_spider\Other\spider_all\Certificate\税务非正常户\excle','非正常户认定公告（201912）.xlsx')
        print(path)
        workbook = open_workbook(path)  # 打开excel文件
        sheet2 = workbook.sheet_by_index(0)
        print(sheet2.nrows)
        # col = 0
        # row = 0
        #
        # try:
        #     for i in range(0, 7):
        #         try:
        #             for j in range(0, 4):
        #                 title = sheet2.cell(i, j).value
        #                 if title == '纳税人名称':
        #                     print(i, j)
        #                     col = j
        #                     row = i
        #                     break
        #         except Exception:
        #             continue
        #         if row!=0:
        #             break
        # except Exception:
        #     pass
        try:
            for i in range(6, sheet2.nrows):
                company_name = sheet2.cell(i, 2).value

                # date = sheet2.cell(i,6).value
                # if '2020' not in date and '2019' not in date and '2018' not in date:
                #     date = sheet2.cell(i, 7).value

                date = date
                # date = '201912'
                if str(date).endswith('.0'):
                    from datetime import datetime
                    from xlrd import xldate_as_tuple
                    date = datetime(*xldate_as_tuple(date, 0))
                    date = date.strftime('%Y-%m-%d')
                if company_name:
                    print(company_name,date)
                    medicine = Medicine(company_name=company_name,area=9,abnormal_date=date)
                    session.add(medicine)
        except Exception as e:
            print(e)
            print('有问题',d)
        # break
    # session.commit()

def parse_docx():
    import docx
    import os
    area = '缙云县'
    all_data = os.listdir(r'D:\projects\Spider\local_spider\Other\spider_all\Certificate\税务非正常户\{}'.format(area))
    for i in all_data:

        # if i!='国家税务总局湖州市南浔区税务局企业非正常户公告（2020）1号':
        #     continue
        if '.docx'  not in i:
            continue
        import re
        ddd = re.findall(r'.*（(.*?)年(.*?)月',i)
        year = ddd[0][0]
        month = ddd[0][1]
        # month = str(int(month) - 1)
        # if month == '0':
        #     year = str(int(year) - 1)
        #     month = '12'
        if len(month) == 1:
            month = '0' + month
        date = year + month
        data = docx.Document(r'D:\projects\Spider\local_spider\Other\spider_all\Certificate\税务非正常户\{}\{}'.format(area,i))
        all_tables = data.tables
        for ta in all_tables:
            rows = ta.rows
            for j in range(1, len(rows)):
                company_name = ta.cell(j, 0).text.replace('\n','')
                # date = ta.cell(j, 7).text.replace('\n','')
                # date = '201901'
                date=date
                print(company_name,date)
                medicine = Medicine(company_name=company_name, area=9, abnormal_date=date)
                session.add(medicine)
        # session.commit()

if __name__ == '__main__':
    # parse_docx()
    parse_excle()
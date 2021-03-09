# import time,re,json
# import threading
# from lxml import etree
# import requests,pymysql
# from sqlalchemy import Column, String, create_engine, Integer
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy import or_
# from sqlalchemy.ext.declarative import declarative_base
# # 创建对象的基类:
# Base = declarative_base()
# # 定义User对象:
# class Medicine(Base):
#     # 表的名字:
#     __tablename__ = 'spider_2_revoke_model_50000'
#
#     # 表的结构:
#     id = Column(Integer(), primary_key=True, autoincrement=True)
#     company_name = Column(String(256))
#     business_status = Column(String(256))
#     connect_company_count = Column(String(256))
#     busi_risk_count = Column(String(256))
#     busi_abnormal_situation = Column(String(256))
#     easy_revoke_end_date = Column(String(256))
#     easy_revoke_result = Column(String(256))
#     risk_date = Column(String(256))
#     risk_reason = Column(String(256))
#     is_have_year_report = Column(String(256))
#     year_report_url = Column(String(256))
#     year_report_busi_status = Column(String(256))
#     nineteen_insurance_count = Column(String(256))
#     eighteen_insurance_count = Column(String(256))
#     seventeen_insurance_count = Column(String(256))
#     company_id = Column(String(256))
# # 初始化数据库连接:
# engine = create_engine('mysql+pymysql://root:BOOT-xwork1024@192.168.2.97:3306/spider')
# # 创建DBSession类型:
# DBSession = sessionmaker(bind=engine)
# # 创建session对象:
# session = DBSession()
#
# class Medicine1(Base):
#     # 表的名字:
#     __tablename__ = 'company_business_risk'
#
#     # 表的结构:
#     id = Column(Integer(), primary_key=True, autoincrement=True)
#
#     included_date = Column(String(256))
#     included_reasons = Column(String(256))
#     included_organ = Column(String(256))
#     removal_date = Column(String(256))
#     removal_reasons = Column(String(256))
#     removal_organ = Column(String(256))
#     company_id = Column(String(256))
#
#
# data = session.query(Medicine).all()
# print(len(data))
# for index,i in enumerate(data):
#     print(index)
#     company_id = i.company_id
#     busi_risk = session.query(Medicine1).filter(Medicine1.company_id == company_id).all()
#     sum = []
#     for risk in busi_risk:
#         single = {}
#         included_date = str(risk.included_date)
#         included_reasons = risk.included_reasons
#         included_organ = risk.included_organ
#         removal_date = str(risk.removal_date)
#         removal_reasons = risk.removal_reasons
#         removal_organ = risk.removal_organ
#         single['列入日期'] = included_date
#         single['列入原因'] = included_reasons
#         single['列入机关'] = included_organ
#         single['移出日期'] = removal_date
#         single['移出原因'] = removal_reasons
#         single['移出机关'] = removal_organ
#         sum.append(single)
#     i.busi_abnormal_situation = str(sum)
#     i.busi_risk_count= len(busi_risk)
# session.commit()
'''
将数据进行指标扫描，得到命中指标的数据
'''
import json
from sqlalchemy import Column, String, create_engine, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# 创建对象的基类:
Base = declarative_base()
# 定义User对象:
class Medicine(Base):
    # 表的名字:
    __tablename__ = 'spider_2_revoke_model_second'

    # 表的结构:
    id = Column(Integer(), primary_key=True, autoincrement=True)
    company_name = Column(String(256))
    business_status = Column(String(256))
    business_term = Column(String(256))
    connect_company_count = Column(String(256))
    busi_risk_count = Column(String(256))
    busi_abnormal_situation = Column(String(256))
    apply_date= Column(String(256))
    own_tax_money = Column(String(256))
    easy_revoke_end_date = Column(String(256))
    easy_revoke_result = Column(String(256))
    risk_date = Column(String(256))
    risk_reason = Column(String(256))
    is_have_year_report = Column(String(256))
    is_parasitic_addr = Column(String(256))
    is_administrative_sanction = Column(String(256))
    abnormal_new_tax_status = Column(String(256))
    year_report_url = Column(String(256))
    nineteen_insurance_count = Column(String(256))
    eighteen_insurance_count = Column(String(256))
    seventeen_insurance_count = Column(String(256))
    busi_status_update = Column(String(256))
    current_1_busi_status = Column(String(256))
    current_2_busi_status = Column(String(256))
    company_id = Column(String(256))
    condition_1 = Column(String(256))
    condition_2 = Column(String(256))
    condition_3 = Column(String(256))
    condition_4 = Column(String(256))
    condition_5 = Column(String(256))
    condition_6 = Column(String(256))
    condition_7 = Column(String(256))
    condition_8 = Column(String(256))
    condition_9 = Column(String(256))
    condition_10 = Column(String(256))
    condition_11 = Column(String(256))
    condition_12 = Column(String(256))
    condition_13 = Column(String(256))
    condition_14 = Column(String(256))
    condition_15 = Column(String(256))


# 初始化数据库连接:
engine = create_engine('mysql+pymysql://root:BOOT-xwork1024@192.168.2.97:3306/spider')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
# 创建session对象:
session = DBSession()

def main():
    # 经营期限到期
    # data = session.query(Medicine).filter(Medicine.business_status != None).all()
    # for d in data:
    #     busi_status = d.business_status
    #     business_term = d.business_term
    #     company_name = d.company_name
    #
    #     if busi_status in '在业/在营/存续/开业/正常/停业' and business_term != None:
    #         if '9999' not in business_term and '无固定期限' not in business_term:
    #             # print(business_term.split('至')[-1][:4])
    #             if business_term =='-':
    #                 continue
    #             year = int(business_term.split('至')[-1][:4])
    #             if year <= 2021:
    #                 print(year,company_name)
    #                 medicine = session.query(Medicine).filter(Medicine.company_name == company_name).first()
    #                 medicine.condition_1 = 1
    # session.commit()

    # 吊销未注销
    # data = session.query(Medicine).filter(Medicine.is_administrative_sanction == 1).all()
    # for d in data:
    #     company_name = d.company_name
    #     busi_status = d.business_status
    #     busi_abnormal_situation = d.busi_abnormal_situation
    #     print(company_name,busi_status)
    #     # if '未注销' in busi_status:
    #     #     d.busi_status_update = '吊销，未注销'
    #     # elif '已注销' in busi_status:
    #     #     d.busi_status_update = '吊销，已注销'
    #
    #     # 第二种原因
    #     if busi_abnormal_situation == None:
    #         continue
    #     if '企业注销，自动移出' in busi_abnormal_situation:
    #         d.busi_status_update = '吊销，已注销'
    # session.commit()

    # data = session.query(Medicine).filter(Medicine.busi_status_update == '吊销，未注销').all()
    # for d in data:
    #     d.condition_2 = 1
    # session.commit()

    # 清算、停业歇业、长期处于筹建
    # data = session.query(Medicine).all()
    # for d in data:
    #     current_1_busi_status = d.current_1_busi_status
    #     current_2_busi_status = d.current_2_busi_status
    #     if current_1_busi_status == '正在清算中' or current_1_busi_status == '停业、歇业'or current_1_busi_status == '歇业'or current_1_busi_status == '停业':
    #         d.condition_3 = 1
    #     elif current_1_busi_status == '筹建' and current_2_busi_status == '筹建':
    #         d.condition_3 = 1
    # session.commit()

    # data = session.query(Medicine).filter(Medicine.apply_date < '2019-06-30').all()
    # for d in data:
    #     company_name = d.company_name
    #     current_1_busi_status = d.current_1_busi_status
    #     apply_date = str(d.apply_date)
    #     apply_date = apply_date.split('-')[0]
    #     if  apply_date == '2019' and current_1_busi_status == '筹建':
    #         d.condition_3 = 1
    #         print(apply_date,company_name)
    #
    # session.commit()
    # 最近1年无社保
    # data = session.query(Medicine).filter(Medicine.nineteen_insurance_count == '0人').all()
    # for d in data:
    #     d.condition_4 = 1
    # session.commit()

    # 最近2年无社保
    # data = session.query(Medicine).filter(Medicine.nineteen_insurance_count == '0人' ).all()
    # for d in data:
    #     eighteen_insurance_count = d.eighteen_insurance_count
    #     if eighteen_insurance_count == '0人':
    #         d.condition_5 = 1
    # session.commit()

    # 最近3年无社保
    # data = session.query(Medicine).filter(Medicine.nineteen_insurance_count == '0人').all()
    # for d in data:
    #     eighteen_insurance_count = d.eighteen_insurance_count
    #     seventeen_insurance_count = d.seventeen_insurance_count
    #     if eighteen_insurance_count == '0人' and seventeen_insurance_count == '0人':
    #         d.condition_6 = 1
    # session.commit()
    # 税务非正常
    # data = session.query(Medicine).filter(Medicine.abnormal_new_tax_status == '非正常').all()
    # for d in data:
    #     company_name = d.company_name
    #     d.condition_7 = 1
    #     print(company_name)
    # session.commit()

    # 税务欠税
    # data = session.query(Medicine).filter(Medicine.own_tax_money != None).all()
    # for d in data:
    #     company_name = d.company_name
    #     own_tax_money = d.own_tax_money
    #     if own_tax_money != '0.00':
    #         d.condition_8 = 1
    #         print(company_name, own_tax_money)
    # session.commit()

    # 存在地址异常未处理
    # data = session.query(Medicine).filter(Medicine.busi_abnormal_situation != '[]').all()
    # print(len(data))
    # for d in data:
    #
    #     company_name = d.company_name
    #     busi_abnormal_situation = d.busi_abnormal_situation
    #     busi_abnormal_situation = eval(busi_abnormal_situation)
    #
    #     for busi in busi_abnormal_situation:
    #         print(company_name,busi)
    #         in_reason = str(busi['列入原因'])
    #         out_date = str(busi['移出日期'])
    #         out_reason =str(busi['移出原因'])
    #         if '通过登记的住所或者经营场所无法联系的' == in_reason and out_date == 'None' :
    #             d.condition_9 = 1
    #             print(company_name, '第一种地址异常')
    #
    #         elif '通过登记的住所或者经营场所无法联系的' == in_reason and out_reason == '列入经营异常名录届满3年仍未履行公示义务的，列入严重违法企业名单，自动移出':
    #             d.condition_9 = 1
    #             print(company_name, '第二种地址异常')
    #
    # session.commit()

    # 存在连续两年地址异常未处理  0个
    # data = session.query(Medicine).filter(Medicine.busi_abnormal_situation != '[]').all()
    # print(len(data))
    # for d in data:
    #     flag = 0
    #     company_name = d.company_name
    #     busi_abnormal_situation = eval(d.busi_abnormal_situation)
    #     for busi in busi_abnormal_situation:
    #         in_reason = str(busi['列入原因'])
    #         in_date = str(busi['列入日期'])
    #         out_date = str(busi['移出日期'])
    #         out_reason = str(busi['移出原因'])
    #         print(in_date)
    #         if in_date == '-':
    #             continue
    #         if in_date != 'None':
    #             year = int(in_date.split('-')[0])
    #
    #             if '通过登记的住所或者经营场所无法联系的' == in_reason and out_date == 'None' :
    #                 if flag == year-1:
    #                     d.condition_10 = 1
    #                     print(company_name,'连续两年地址异常')
    #                 flag = year
    #             elif '通过登记的住所或者经营场所无法联系的' == in_reason and out_reason == '列入经营异常名录届满3年仍未履行公示义务的，列入严重违法企业名单，自动移出':
    #                 if flag == year-1:
    #                     d.condition_10 = 1
    #                     print(company_name,'连续两年地址异常')
    #                 flag = year
    # session.commit()

    # 挂靠地址异常未处理
    # data = session.query(Medicine).filter(Medicine.is_parasitic_addr == 1).all()
    # print(len(data))
    # for d in data:
    #     company_name = d.company_name
    #     condition_9 = d.condition_9
    #     if condition_9:
    #         d.condition_11 = 1
    #         print(company_name)
    #
    # session.commit()

    # 存在年报异常未处理
    # data = session.query(Medicine).filter(Medicine.busi_abnormal_situation != '[]').all()
    # print(len(data))
    # for d in data:
    #     company_name = d.company_name
    #     busi_abnormal_situation = eval(d.busi_abnormal_situation)
    #     for busi in busi_abnormal_situation:
    #         in_reason = str(busi['列入原因'])
    #         out_date = str(busi['移出日期'])
    #         out_reason = str(busi['移出原因'])
    #         if '《企业信息公示暂行条例》第八条规定' in in_reason and out_date == 'None' :
    #             d.condition_12 = 1
    #             print(company_name, '年报异常')
    #
    #         elif '《企业信息公示暂行条例》第八条规定' == in_reason and out_reason == '列入经营异常名录届满3年仍未履行公示义务的，列入严重违法企业名单，自动移出':
    #             d.condition_12 = 1
    #             print(company_name, '年报异常')
    #
    # session.commit()

    # 存在连续两年年报异常未处理
    # data = session.query(Medicine).filter(Medicine.busi_abnormal_situation != '[]').all()
    # print(len(data))
    # for d in data:
    #     flag = 0
    #     company_name = d.company_name
    #     busi_abnormal_situation = eval(d.busi_abnormal_situation)
    #     for busi in busi_abnormal_situation:
    #         in_reason = str(busi['列入原因'])    #  'None'  和 None 不一样的
    #         in_date = str(busi['列入日期'])
    #         out_date = str(busi['移出日期'])
    #         out_reason = str(busi['移出原因'])
    #         print(in_date)
    #         if in_date == '-':
    #             continue
    #         if in_date != 'None':
    #             year = int(in_date.split('-')[0])
    #
    #             if '《企业信息公示暂行条例》第八条' in in_reason and out_date == 'None' :
    #                 if flag == year+1:
    #                     d.condition_13 = 1
    #                     print(company_name,'连续两年年报异常')
    #                 flag = year
    #             elif '《企业信息公示暂行条例》第八条' in in_reason and out_reason == '列入经营异常名录届满3年仍未履行公示义务的，列入严重违法企业名单，自动移出':
    #                 if flag == year+1:
    #                     d.condition_13 = 1
    #                     print(company_name,'连续两年年报异常')
    #                 flag = year
    #
    # session.commit()

    # 关联公司经营异常
    # data = session.query(Medicine).filter(Medicine.connect_company_count >=3 ).all()
    # print(len(data))
    # for d in data:
    #     company_name = d.company_name
    #     count = d.connect_company_count
    #     condition_9 = d.condition_9
    #     condition_12 = d.condition_12
    #     if condition_9 or condition_12:
    #         print('company_name',company_name,'count',count,'condition_9',condition_9,'condition_12',condition_12)
    #         d.condition_14 = 1
    #
    # session.commit()
    # 简易注销公示完未处理
    # data = session.query(Medicine).filter(Medicine.easy_revoke_end_date < '2020-11-10' ).all()
    # print(len(data))
    # for d in data:
    #     company_name = d.company_name
    #     easy_revoke_end_date = d.easy_revoke_end_date
    #     easy_revoke_result = d.easy_revoke_result
    #     if '正在进行简易注销公告' == easy_revoke_result or '不予受理' ==easy_revoke_result:
    #         d.condition_15 = 1
    #         print(company_name,easy_revoke_end_date,easy_revoke_result)
    # session.commit()

    # 是否真实联系方式（就是注册时间19年7月1号前，有号码就有，没有就算了）
    pass
if __name__ == '__main__':
    main()
from sqlalchemy import Column, String, create_engine, Integer,and_
from sqlalchemy.ext.declarative import declarative_base
# 创建对象的基类:
Base = declarative_base()


class table_icp_leads(Base):
    # 表的名字:
    __tablename__ = 'icp_leads'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    site_domain = Column(String(256))
    company_name = Column(String(256))
    main_page = Column(String(256))
    site_license = Column(String(256))
    site_name = Column(String(256))

    company_type = Column(String(256))
    phone = Column(String(256))
    verify_time = Column(String(256))
    dns_provider = Column(String(256))

    eg_capital = Column(String(256))
    social_staff_num = Column(String(256))
    business_scope = Column(String(256))
    company_org_type = Column(String(256))
    phone_source = Column(String(256))
    gmt_created = Column(String(256))
    gmt_updated = Column(String(256))



class table_company_info(Base):
    # 表的名字:
    __tablename__ = 'company_info'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    company_name = Column(String(256))
    reg_money = Column(String(256))
    insurance_num = Column(String(256))
    business_project = Column(String(256))
    company_type = Column(String(256))

    mobile = Column(String(256))
    mobiles = Column(String(256))




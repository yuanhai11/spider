# import pymysql
# import pickle
#
# db = pymysql.connect(host="localhost", user="root", password='123456', database="spider", port=3306)
# cursor = db.cursor()
#
# # sql = "select id,company_name from company_info"
# #
# # cursor.execute(sql)
# # data = cursor.fetchall()
# # all_data = {}
# # for d in data:
# #     id = d[0]
# #     name = d[1]
# #     all_data[name] = id
# # # print(all_data)
# # print(len(all_data))
# # # exit()
# # f = open('cache','wb')
# # pickle.dump(all_data,f)
# # exit()
# #

# # from cacheout import Cache
# # cache = Cache(maxsize=1000000000000000)
# # for i in data:
# #     cache.set(i[1],i[0])
# # print(cache.get('Q杭州五科科技有限公司海宁分公司'))
# # exit()
# # data = [i for i in data if i[1]!=None]
# # print(data)
# # print(len(list(set(data))))
#
# # exit()
# #
# f = open('cache','rb')
# data = pickle.load(f)
# print(len(data))
#
# sql1 = "select company_name from spider_company_related_park"
#
# cursor.execute(sql1)
# sql_data = cursor.fetchall()
# sql_data = [i[0] for i in sql_data]
# sql_data = list(set(sql_data))
# exit()


# sum = []
# for i in sql_data:
#     print(i)
#     id = data.get(i)
#     if id:
#         sum.append((id,i))
# print(len(sum))
# exit()

# for db in sum:
#     id = db[0]
#     name = db[1]
#     print(name)
#     sql = """update spider_company_related_park set company_id='{}' where company_name='{}'""".format(id,name)
#     cursor.execute(sql)
# db.commit()
# db.close()

'''
批量更新SQL：inner join 只查出来有关联的数据
            left join 查出左表有的所有数据，即便右边为空
    ' update spider_company_related_park left join company_info on company_info.company_name=spider_company_related_park.company_name set spider_company_related_park.company_id=company_info.id;'
'''

# sql = 'update spider_high_talent left join company_info on company_info.company_name=spider_high_talent.company set spider_high_talent.company_id=company_info.id;'
# sql = 'update {} left join company_info on company_info.company_name={}.company_name set {}.company_id=company_info.id;'
# data = ['spider_add_value_telecom_info', 'spider_baiduzp', 'spider_brand', 'spider_company_honor_data', 'spider_company_makerspace', 'spider_company_related_park', 'spider_culture_business_license', 'spider_high_talent', 'spider_industry_information', 'spider_notice', 'spider_outstand_talent', 'spider_park_data', 'spider_park_data_qianzhan', 'spider_radio_show_business_license', 'spider_service_license', 'spider_sh_company_cosmetic_produce', 'spider_sh_company_customized_medical_equipment', 'spider_sh_company_first_medical_equipment_produce', 'spider_sh_company_medical_equipment_business', 'spider_sh_company_medical_equipment_entrust_produce', 'spider_sh_company_medical_equipment_license_invalid', 'spider_sh_company_medical_equipment_network_sale', 'spider_sh_company_medical_equipment_network_third_party_platform', 'spider_sh_company_medicine_company', 'spider_sh_company_medicine_produce', 'spider_sh_company_two_three_medical_equipment_produce', 'spider_sh_product_first_medical_equipment_product', 'spider_sh_product_hospital_preparation_product', 'spider_sh_product_medical_traditional_chinese_medicine', 'spider_sh_product_medicine', 'spider_sh_product_medicine_accessories', 'spider_sh_product_medicine_packaging_material', 'spider_sh_product_two_medical_equipment_product', 'spider_sh_ralated_GMP_license', 'spider_sh_related_GSP_license', 'spider_sh_related_european_proval_file', 'spider_sh_related_internet_medicine_msg_server', 'spider_sh_related_internet_medicine_transaction_server', 'spider_sh_related_medical_equipment_produce_export_sale_prove', 'spider_sh_related_medicine_export_sale_prove', 'spider_sh_related_medicine_produce_license', 'spider_sh_related_vending_machine', 'spider_talent_room', 'spider_tax', 'spider_zj_company_cosmetic', 'spider_zj_company_medical_equipment', 'spider_zj_company_medicine', 'spider_zj_people_cosmetic', 'spider_zj_people_medical_equipment', 'spider_zj_people_medicine', 'spider_zj_product_cosmetic', 'spider_zj_product_medical_equipment', 'spider_zj_product_medicine']
# for i in data:
#     print(sql.format(i,i,i))


'''
update spider_add_value_telecom_info left join company_info on company_info.company_name=spider_add_value_telecom_info.company_name set spider_add_value_telecom_info.company_id=company_info.id;
update spider_culture_business_license left join company_info on company_info.company_name=spider_culture_business_license.company_name set spider_culture_business_license.company_id=company_info.id;
update spider_high_talent left join company_info on company_info.company_name=spider_high_talent.company_name set spider_high_talent.company_id=company_info.id;
update spider_industry_information left join company_info on company_info.company_name=spider_industry_information.company_name set spider_industry_information.company_id=company_info.id;
update spider_radio_show_business_license left join company_info on company_info.company_name=spider_radio_show_business_license.company_name set spider_radio_show_business_license.company_id=company_info.id;
update spider_service_license left join company_info on company_info.company_name=spider_service_license.company_name set spider_service_license.company_id=company_info.id;
update spider_sh_company_cosmetic_produce left join company_info on company_info.company_name=spider_sh_company_cosmetic_produce.company_name set spider_sh_company_cosmetic_produce.company_id=company_info.id;
update spider_sh_company_customized_medical_equipment left join company_info on company_info.company_name=spider_sh_company_customized_medical_equipment.company_name set spider_sh_company_customized_medical_equipment.company_id=company_info.id;
update spider_sh_company_first_medical_equipment_produce left join company_info on company_info.company_name=spider_sh_company_first_medical_equipment_produce.company_name set spider_sh_company_first_medical_equipment_produce.company_id=company_info.id;
update spider_sh_company_medical_equipment_business left join company_info on company_info.company_name=spider_sh_company_medical_equipment_business.company_name set spider_sh_company_medical_equipment_business.company_id=company_info.id;
update spider_sh_company_medical_equipment_entrust_produce left join company_info on company_info.company_name=spider_sh_company_medical_equipment_entrust_produce.company_name set spider_sh_company_medical_equipment_entrust_produce.company_id=company_info.id;
update spider_sh_company_medical_equipment_license_invalid left join company_info on company_info.company_name=spider_sh_company_medical_equipment_license_invalid.company_name set spider_sh_company_medical_equipment_license_invalid.company_id=company_info.id;
update spider_sh_company_medical_equipment_network_sale left join company_info on company_info.company_name=spider_sh_company_medical_equipment_network_sale.company_name set spider_sh_company_medical_equipment_network_sale.company_id=company_info.id;
update spider_sh_company_medical_equipment_network_third_party_platform left join company_info on company_info.company_name=spider_sh_company_medical_equipment_network_third_party_platform.company_name set spider_sh_company_medical_equipment_network_third_party_platform.company_id=company_info.id;
update spider_sh_company_medicine_company left join company_info on company_info.company_name=spider_sh_company_medicine_company.company_name set spider_sh_company_medicine_company.company_id=company_info.id;
update spider_sh_company_medicine_produce left join company_info on company_info.company_name=spider_sh_company_medicine_produce.company_name set spider_sh_company_medicine_produce.company_id=company_info.id;
update spider_sh_company_two_three_medical_equipment_produce left join company_info on company_info.company_name=spider_sh_company_two_three_medical_equipment_produce.company_name set spider_sh_company_two_three_medical_equipment_produce.company_id=company_info.id;
update spider_sh_product_first_medical_equipment_product left join company_info on company_info.company_name=spider_sh_product_first_medical_equipment_product.company_name set spider_sh_product_first_medical_equipment_product.company_id=company_info.id;
update spider_sh_product_hospital_preparation_product left join company_info on company_info.company_name=spider_sh_product_hospital_preparation_product.company_name set spider_sh_product_hospital_preparation_product.company_id=company_info.id;
update spider_sh_product_medical_traditional_chinese_medicine left join company_info on company_info.company_name=spider_sh_product_medical_traditional_chinese_medicine.company_name set spider_sh_product_medical_traditional_chinese_medicine.company_id=company_info.id;
update spider_sh_product_medicine left join company_info on company_info.company_name=spider_sh_product_medicine.company_name set spider_sh_product_medicine.company_id=company_info.id;
update spider_sh_product_medicine_accessories left join company_info on company_info.company_name=spider_sh_product_medicine_accessories.company_name set spider_sh_product_medicine_accessories.company_id=company_info.id;
update spider_sh_product_medicine_packaging_material left join company_info on company_info.company_name=spider_sh_product_medicine_packaging_material.company_name set spider_sh_product_medicine_packaging_material.company_id=company_info.id;
update spider_sh_product_two_medical_equipment_product left join company_info on company_info.company_name=spider_sh_product_two_medical_equipment_product.company_name set spider_sh_product_two_medical_equipment_product.company_id=company_info.id;
update spider_sh_ralated_GMP_license left join company_info on company_info.company_name=spider_sh_ralated_GMP_license.company_name set spider_sh_ralated_GMP_license.company_id=company_info.id;
update spider_sh_related_GSP_license left join company_info on company_info.company_name=spider_sh_related_GSP_license.company_name set spider_sh_related_GSP_license.company_id=company_info.id;
update spider_sh_related_european_proval_file left join company_info on company_info.company_name=spider_sh_related_european_proval_file.company_name set spider_sh_related_european_proval_file.company_id=company_info.id;
update spider_sh_related_internet_medicine_msg_server left join company_info on company_info.company_name=spider_sh_related_internet_medicine_msg_server.company_name set spider_sh_related_internet_medicine_msg_server.company_id=company_info.id;
update spider_sh_related_internet_medicine_transaction_server left join company_info on company_info.company_name=spider_sh_related_internet_medicine_transaction_server.company_name set spider_sh_related_internet_medicine_transaction_server.company_id=company_info.id;
update spider_sh_related_medical_equipment_produce_export_sale_prove left join company_info on company_info.company_name=spider_sh_related_medical_equipment_produce_export_sale_prove.company_name set spider_sh_related_medical_equipment_produce_export_sale_prove.company_id=company_info.id;
update spider_sh_related_medicine_export_sale_prove left join company_info on company_info.company_name=spider_sh_related_medicine_export_sale_prove.company_name set spider_sh_related_medicine_export_sale_prove.company_id=company_info.id;
update spider_sh_related_medicine_produce_license left join company_info on company_info.company_name=spider_sh_related_medicine_produce_license.company_name set spider_sh_related_medicine_produce_license.company_id=company_info.id;
update spider_sh_related_vending_machine left join company_info on company_info.company_name=spider_sh_related_vending_machine.company_name set spider_sh_related_vending_machine.company_id=company_info.id;
update spider_talent_room left join company_info on company_info.company_name=spider_talent_room.company_name set spider_talent_room.company_id=company_info.id;
update spider_zj_company_cosmetic left join company_info on company_info.company_name=spider_zj_company_cosmetic.company_name set spider_zj_company_cosmetic.company_id=company_info.id;
update spider_zj_company_medical_equipment left join company_info on company_info.company_name=spider_zj_company_medical_equipment.company_name set spider_zj_company_medical_equipment.company_id=company_info.id;
update spider_zj_company_medicine left join company_info on company_info.company_name=spider_zj_company_medicine.company_name set spider_zj_company_medicine.company_id=company_info.id;
update spider_zj_people_cosmetic left join company_info on company_info.company_name=spider_zj_people_cosmetic.company_name set spider_zj_people_cosmetic.company_id=company_info.id;
update spider_zj_people_medical_equipment left join company_info on company_info.company_name=spider_zj_people_medical_equipment.company_name set spider_zj_people_medical_equipment.company_id=company_info.id;
update spider_zj_people_medicine left join company_info on company_info.company_name=spider_zj_people_medicine.company_name set spider_zj_people_medicine.company_id=company_info.id;
update spider_zj_product_cosmetic left join company_info on company_info.company_name=spider_zj_product_cosmetic.company_name set spider_zj_product_cosmetic.company_id=company_info.id;
update spider_zj_product_medical_equipment left join company_info on company_info.company_name=spider_zj_product_medical_equipment.company_name set spider_zj_product_medical_equipment.company_id=company_info.id;
update spider_zj_product_medicine left join company_info on company_info.company_name=spider_zj_product_medicine.company_name set spider_zj_product_medicine.company_id=company_info.id;
'''

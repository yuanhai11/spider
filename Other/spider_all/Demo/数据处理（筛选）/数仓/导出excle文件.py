import json

def parse_excle():
    import xlwt
    # 创建一个Wordbook对象，相当于创建了一个Excel文件
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)
    # 创建一个sheet对象，一个sheet对象对应Excel文件中的一张表格
    sheet = book.add_sheet("result", cell_overwrite_ok=True)

    with open('data1.txt',encoding='utf-8')as f:
        con = f.readlines()
    num = 1
    for i in con:
        i = json.loads(i)
        company_name = i['company_name']
        insurance_num = i['insurance_num']
        reg_date= i['reg_date']
        phone= i['phone']
        company_status= i['company_status']
        company_type= i['company_type'].strip()

        phone = ','.join([i['pN'] for i in json.loads(phone)])

        sum = [company_name, insurance_num,reg_date,phone,company_status,company_type]
        for index, s in enumerate(sum):
            sheet.write(num, index, s)  #
        num += 1

    book.save("data__result.xls")
if __name__ == '__main__':
    parse_excle()
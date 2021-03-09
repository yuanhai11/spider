from xlrd import open_workbook
import pandas as pd

def kaoqin():
    '''
    description:考勤表制作
    :keyword: 1:迟到早退 2：漏打卡 3：事假 4：病假 5：调休年假产检假  6：孕妇 7：外出 8：加班 9：不明情况
     通过xlrd 操作excle
    :return:
    '''
    workbook = open_workbook(
        r'/Demo/杭州罗实信息技术有限公司_打卡时间表_20201001-20201031_1.xlsx')  # 打开excel文件
    sheet2 = workbook.sheet_by_index(0)
    a = sheet2.row_values(2)
    print(a)
    exit()
    a = sheet2._xf_index_stats
    print(a)
    exit()


    a = sheet2.row_values(2)[6:]
    sum = []
    for pa in range(7,164):
        b = sheet2.row_values(pa)[6:]
        sum.append(b)
    for index,i in enumerate(sum):
            for indexxx,jjj in enumerate(a):
                if jjj == '六':
                    if i[indexxx]:
                        print('周六有加班的坐标：({},{})'.format(index+1,indexxx+1),end='\t\t')
            print()

if __name__ == '__main__':
    kaoqin()

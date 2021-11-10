# import os
#
#
#
# lists = os.listdir(r'C:\Users\20945\Desktop\考试\2021初级人力职称精讲（第二轮）讲义合集\2021初级人力职称精讲（第二轮）讲义合集')
#
# lists = [i for i in lists if "课件" not in i]
# print(lists)
# content = b""
# for l in lists:
#     with open(r'C:\Users\20945\Desktop\考试\2021初级人力职称精讲（第二轮）讲义合集\2021初级人力职称精讲（第二轮）讲义合集\\'+l,'rb')as fp:
#         content += fp.read()
# with open('merge.pdf','wb')as f:
#     f.write(content)

# -*- coding:utf-8*-
# 利用PyPDF2模块合并同一文件夹下的所有PDF文件
# 只需修改存放PDF文件的文件夹变量：file_dir 和 输出文件名变量: outfile

import os
from PyPDF2 import PdfFileReader, PdfFileWriter
import time


# 使用os模块的walk函数，搜索出指定目录下的全部PDF文件
# 获取同一目录下的所有PDF文件的绝对路径
def getFileName(filedir):
    file_list = [os.path.join(root, filespath) \
                 for root, dirs, files in os.walk(filedir) \
                 for filespath in files \
                 if str(filespath).endswith('pdf') and '课件' not in filespath
                 ]
    return file_list if file_list else []


# 合并同一目录下的所有PDF文件
def MergePDF(filepath, outfile):
    output = PdfFileWriter()
    outputPages = 0
    pdf_fileName = getFileName(filepath)
    pdf_fileName = ['C:\\Users\\20945\\Desktop\\考试\\heih\\2021初级经济基础精讲（第二轮）-1 打印版.pdf',
                    'C:\\Users\\20945\\Desktop\\考试\\heih\\2021初级经济基础精讲（第二轮）-2 打印版.pdf',
                    'C:\\Users\\20945\\Desktop\\考试\\heih\\2021初级经济基础精讲（第二轮）-3 打印版.pdf',
                    'C:\\Users\\20945\\Desktop\\考试\\heih\\2021初级经济基础精讲（第二轮）-4 打印版.pdf',
                    'C:\\Users\\20945\\Desktop\\考试\\heih\\2021初级经济基础精讲（第二轮）-5 打印版.pdf',
                    'C:\\Users\\20945\\Desktop\\考试\\heih\\2021初级经济基础精讲（第二轮）-6 打印版（已打印上次讲义的同学，本次讲义从第5页开始打印即可）.pdf',
                    'C:\\Users\\20945\\Desktop\\考试\\heih\\2021初级经济基础精讲（第二轮）-7 打印版.pdf',
                    'C:\\Users\\20945\\Desktop\\考试\\heih\\2021初级经济基础精讲（第二轮）-8 打印版.pdf',
                    'C:\\Users\\20945\\Desktop\\考试\\heih\\2021初级经济基础精讲（第二轮）-9 打印版.pdf',
                    'C:\\Users\\20945\\Desktop\\考试\\heih\\2021初级经济基础精讲（第二轮）-11 打印版.pdf',
                    'C:\\Users\\20945\\Desktop\\考试\\heih\\2021初级经济基础精讲（第二轮）-12 打印版.pdf',
                    'C:\\Users\\20945\\Desktop\\考试\\heih\\2021初级经济基础精讲（第二轮）-13 打印版.pdf',
                    'C:\\Users\\20945\\Desktop\\考试\\heih\\2021初级经济基础精讲（第二轮）-14 打印版.pdf',
                    'C:\\Users\\20945\\Desktop\\考试\\heih\\2021初级经济基础精讲（第二轮）-15 打印版.pdf',
                    'C:\\Users\\20945\\Desktop\\考试\\heih\\2021初级经济基础精讲（第二轮）-16 打印版.pdf',
                    'C:\\Users\\20945\\Desktop\\考试\\heih\\2021初级经济基础精讲（第二轮）-17 打印版.pdf',
                    'C:\\Users\\20945\\Desktop\\考试\\heih\\2021初级经济基础精讲（第二轮）-18 打印版.pdf',
                    'C:\\Users\\20945\\Desktop\\考试\\heih\\2021初级经济基础精讲（第二轮）-19 打印版.pdf',
                    'C:\\Users\\20945\\Desktop\\考试\\heih\\2021初级经济基础精讲（第二轮）-20 打印版.pdf',
                    'C:\\Users\\20945\\Desktop\\考试\\heih\\2021初级经济基础精讲（第二轮）-21 22 打印版.pdf',
                    'C:\\Users\\20945\\Desktop\\考试\\heih\\2021初级经济基础精讲（第二轮）-23 打印版.pdf',
                    ]

    print(pdf_fileName)
    if pdf_fileName:
        for pdf_file in pdf_fileName:
            print("路径：%s" % pdf_file)

            # 读取源PDF文件
            input = PdfFileReader(open(pdf_file, "rb"))

            # 获得源PDF文件中页面总数
            pageCount = input.getNumPages()
            outputPages += pageCount
            print("页数：%d" % pageCount)

            # 分别将page添加到输出output中
            for iPage in range(pageCount):
                output.addPage(input.getPage(iPage))

        print("合并后的总页数:%d." % outputPages)
        # 写入到目标PDF文件
        outputStream = open(os.path.join(filepath, outfile), "wb")
        output.write(outputStream)
        outputStream.close()
        print("PDF文件合并完成！")

    else:
        print("没有可以合并的PDF文件！")


# 主函数
def main():
    time1 = time.time()
    file_dir = r'C:\Users\20945\Desktop\考试\heih'  # 存放PDF的原文件夹
    outfile = "Cheat_Sheets-经济.pdf"  # 输出的PDF文件的名称
    MergePDF(file_dir, outfile)
    time2 = time.time()
    print('总共耗时：%s s.' % (time2 - time1))


main()

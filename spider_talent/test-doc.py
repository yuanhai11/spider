from win32com import client as wc
import os
# word = wc.Dispatch("Word.Application")
#
# path = os.path.abspath('.').split('.')[0]+r'\file3333.docx'
# print(path)
# # 必须是绝对路径
# files = word.Documents.Open('{}'.format(path))
# print(files)
# files.Close()
# word.Quit()
#
# import pydoc
# p = pydoc.getdoc('./file3333.files')
# print(p)
#
# import docx
# print(docx.Document('./file3333.docx'))
# import requests
#
# headers = {
#     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
# }
# result = requests.get('http://hrss.hangzhou.gov.cn/picture/old/file3333.doc',headers=headers).content
#
with open(r'Z:\测试账号.txt', 'r')as fp:
    fp.read()

import shutil, os
shutil.copytree(r'C:\Users\20945\Desktop\RPA\zl-rpa\incomeTaxFiling\0申报流程', r'Z:')

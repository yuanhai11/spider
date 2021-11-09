import xlrd
from flask import Flask, request

app = Flask(__name__)


@app.route("/hello", methods=['POST', 'GET'])
def hello():
    return 'hello'


@app.route("/", methods=['POST', 'GET'])
def filelist1():
    print(request.files)
    file = request.files['file']
    print('file', type(file), file)
    print(file.filename)  # 打印文件名
    f = file.read()  # 文件内容
    data = xlrd.open_workbook(file_contents=f)
    table = data.sheets()[0]
    names = data.sheet_names()  # 返回book中所有工作表的名字
    status = data.sheet_loaded(names[0])  # 检查sheet1是否导入完毕
    print(status)
    nrows = table.nrows  # 获取该sheet中的有效行数
    ncols = table.ncols  # 获取该sheet中的有效列数
    print(nrows)
    print(ncols)
    s = table.col_values(0)  # 第1列数据
    for i in s:
        ii = i.strip()
        print(len(ii))

    return 'OK'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000)

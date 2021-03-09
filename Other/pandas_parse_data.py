import pandas as pd
# import ray.dataframe
'''
过滤重复值
chunksize：将文件切块
usecols：读取指定字段在内存中
'''
# df = pd.read_csv('nycflights.txt')
# print(df)
# exit()

columns = ('hour','minute')
df = pd.read_csv('Files_Dir/nycflights.txt', chunksize=1000000, usecols=columns)
# exit()
print(df)
# exit()

for i in df:
    print(i)
    a = i['minute']
    b = a.notnull()
    print(i.loc[(b)])
    # print(a)

    # print(i.query('origin == "JFK" & carrier == "B6"'))
    # print(i.groupby('month').aggregate('count'))
    exit()
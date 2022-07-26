with open("question.txt",encoding='utf-8')as fp:
    content  = fp.readlines()

keys = ["社保","公积金","工资","个税","交税","开票","政策","发票","对账",
"津贴","法人","避税","银行","费用票"]
sum = []
for k in keys:
    single = {}
    single[k] = [i.strip() for i in content if k in i]
    sum.append(single)
print(sum)




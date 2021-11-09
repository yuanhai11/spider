# encoding = utf-8
lis = []
with open('3.txt',encoding='utf-8') as fp:
    content  = str(fp.readlines())
c = content.replace(r'\n','').replace('"','').strip()
c = c.split('，')
for i in c:
    cc = i.split(',')
    for j in cc:
        lis.append(j)

for jj in lis:
    if jj=='':
        continue
    print(jj,"\b")

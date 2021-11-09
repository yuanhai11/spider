import json
with open(r'C:\Users\20945\Desktop\Uibot_project\ICP\data\2.txt',encoding='utf-8') as fp:
    con = fp.read().replace('\n','').replace(' ','').replace('][','----').replace("[","").replace("]",'').split('----')
for i in con:
    print(i)

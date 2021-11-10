import execjs

Passwd = execjs.compile(open(r"boss.js",encoding='utf-8').read()).call('xi')
print (Passwd)

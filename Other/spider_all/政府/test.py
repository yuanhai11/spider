import execjs

Passwd = execjs.compile(open(r"1.js").read()).call('go')
print (Passwd)

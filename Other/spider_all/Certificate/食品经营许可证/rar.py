

from unrar import rarfile


fp = rarfile.RarFile('杭州金诺医学检验所新冠检测须知.rar')
fp.extractall(path='./aaa',pwd='111')

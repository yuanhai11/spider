import os
import re
from Crypto.Cipher import AES
from config import PATTERN, TS_NUM

def check_ts(path):
    # 记录已有的片段
    lst = os.listdir(path)
    ts_idx_list = []
    for item in lst:
        if item.find('.ts') > 0:
            idx = int(re.findall(PATTERN, item)[0])
            ts_idx_list.append(idx)
    # 检查缺失了哪些片段
    for idx in range(0, TS_NUM):
        if not idx in ts_idx_list:
            print(idx)
    print("一共缺少{}个".format(TS_NUM+1-len(ts_idx_list)))
def decode_ts(src, key_path, target):
    '''
    :param src: 单个加密后的ts源文件路径 如 './caches/ntROGW6R4598270.ts'
    :param key_path: 解密key的路径 如 './caches/key.key'
    :param target: 解密后的文件名 如 './results/ntROGW6R4598270.ts'
    :return:
    '''
    raw = open(src, 'rb').read()
    iv = raw[0:16]
    data = raw[16:]
    key = open(key_path, 'rb').read()
    plain_data = AES.new(key, AES.MODE_CBC, iv).decrypt(data) # 解密失败的话可以换一种模式看看
    open(target, 'wb').write(plain_data)

if __name__ == '__main__':
    path = './caches/'
    check_ts(path) # 检查有没有缺失片段
    # 读取缓存批量解密
    lst = os.listdir(path)
    for item in lst:
        if item.find('.ts') > 0 and re.findall(PATTERN, item)[0] >="0": # 后面的条件可以更改解密的开始位置
            decode_ts(path+item, path+'key.key', './results/'+item)
            print(item)

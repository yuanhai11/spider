# coding: utf-8

#当前脚本修改pc状态为空闲      1

import os

def fs():
    lock_file_path = os.path.join(os.getenv("USERPROFILE"),"desktop","lock.txt")
    if os.path.exists(lock_file_path):
        os.remove(lock_file_path)



##目录结构
####worker：负责申报CB系统中浙江的零申报数据
####master：
     task_receive.py（负责接收kafka消息）
     task_scheduler.py（调度器）
    
####rpa-master-manager（接受任务调度，执行任务）
####rpa-master（java重构代码）
## 依赖安装
大部分依赖可以直接访问 [pypi](https://pypi.org/) 安装,只有 pywin32库需要手动下载安装包安装，
建议在系统python 环境安装 虚拟环境安装需要手动 执行 easy_install 安装。
### pywin32 安装
访问 github [项目地址](https://github.com/mhammond/pywin32/releases) 下载227版本的安装包

### crypto 安装
pip install pycryptodome


### worker 模块打包 
在worker 目录下执行一下命令
```bash
python -m PyInstaller --version-file=ver.txt -F work_manager.py

```

### 更新记录
1. worker 消息队列切换为 kafka , rpa-master 弃用
2. rpa-master-manager 采用httpclient的形式。
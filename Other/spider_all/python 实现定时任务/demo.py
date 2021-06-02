from apscheduler.schedulers.blocking import BlockingScheduler

def job():
    import os
    os.mkdir('demo.txt')

scheduler = BlockingScheduler()
scheduler.add_job(job,'cron',)
scheduler.start()

'''
# 资源
https://blog.csdn.net/songlh1234/article/details/82352306
'''
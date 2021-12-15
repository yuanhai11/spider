from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
# 输出时间
def job():
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print(1)
    scheduler.remove_job(job_id='1')

# BlockingScheduler
scheduler = BlockingScheduler()
# scheduler.add_job(job, 'date', day_of_week='1-5', hour=6, minute=30)
scheduler.add_job(job,'interval',seconds=3,id='1')
scheduler.start()

'''
# 资源
https://blog.csdn.net/songlh1234/article/details/82352306
'''
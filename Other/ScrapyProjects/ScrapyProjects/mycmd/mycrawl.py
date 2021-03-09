from scrapy.commands import BaseRunSpiderCommand
from scrapy.exceptions import UsageError

class Command(BaseRunSpiderCommand):

    requires_project = True

    def syntax(self):
        return "[options] <spider>"

    def short_desc(self):
        return "Run a spider"

    def run(self, args, opts):
        # 获取爬虫列表
        spd_loader_list = self.crawler_process.spider_loader.list()
        # 遍历各爬虫
        for spname in spd_loader_list or args:
            self.crawler_process.crawl(spname, **opts.spargs)
            print("此时启动的爬虫：" + spname)
        self.crawler_process.start()


    # def run(self, args, opts):
    #     if len(args) < 1:
    #         raise UsageError()
    #     elif len(args) > 1:
    #         raise UsageError("running 'scrapy crawl' with more than one spider is no longer supported")
    #     spname = args[0]
    #
    #     crawl_defer = self.crawler_process.crawl(spname, **opts.spargs)
    #
    #     if getattr(crawl_defer, 'result', None) is not None and issubclass(crawl_defer.result.type, Exception):
    #         self.exitcode = 1
    #     else:
    #         self.crawler_process.start()
    #
    #         if (
    #             self.crawler_process.bootstrap_failed
    #             or hasattr(self.crawler_process, 'has_exception') and self.crawler_process.has_exception
    #         ):
    #             self.exitcode = 1

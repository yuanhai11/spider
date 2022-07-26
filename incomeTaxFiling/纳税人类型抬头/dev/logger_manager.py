# -*- coding: utf-8 -*-
import os
import logging
import logging.config
import time
from functools import wraps
from logging.handlers import TimedRotatingFileHandler, SMTPHandler

# logging formatter参考
"""
%(name)s            Logger的名字
%(levelno)s         数字形式的日志级别
%(levelname)s       文本形式的日志级别
%(pathname)s        调用日志输出函数的模块的完整路径名，可能没有
%(filename)s        调用日志输出函数的模块的文件名
%(module)s          调用日志输出函数的模块名
%(funcName)s        调用日志输出函数的函数名
%(lineno)d          调用日志输出函数的语句所在的代码行
%(created)f         当前时间，用UNIX标准的表示时间的浮点数表示
%(relativeCreated)d 输出日志信息时的，自Logger创建以来的毫秒数
%(asctime)s         字符串形式的当前时间。默认格式是“2003-07-08 16:49:45,896”。逗号后面的是毫秒
%(thread)d          线程ID。可能没有
%(threadName)s      线程名。可能没有
%(process)d         进程ID。可能没有
%(message)s         用户输出的消息
"""
# with all params
FORMATTER_FULL1 = '[%(hostname)s](%(levelno)s|%(levelname)s)' \
                  '<%(pathname)s %(filename)s %(module)s %(funcName)s %(lineno)d>' \
                  '[%(created)f][%(relativeCreated)d](%(thread)d|%(threadName)s|%(process)d)\n' \
                  '[%(asctime)s](%(levelname)5s)%(name)s : %(message)s'
FORMATTER_FULL1_0 = '[%(hostname)s](%(levelname)s)' \
                    '<%(pathname)s %(filename)s %(module)s %(funcName)s %(lineno)d>' \
                    '[%(created)f][%(relativeCreated)d](%(thread)d|%(threadName)s|%(process)d)\n' \
                    '[%(asctime)s](%(levelname)5s)%(name)s : %(message)s'
# with module&funcName
FORMATTER_FULL2 = '<%(module)s %(funcName)s>(%(thread)d|%(threadName)s|%(process)d)\n' \
                  '[%(asctime)s](%(levelname)5s)(%(thread)d|%(process)d)<%(filename)s:%(lineno)d>%(name)s : %(message)s'
# with thread&process
FORMATTER_FULL3 = '[%(asctime)s](%(levelname)5s)(%(thread)d|%(process)d)<%(filename)s:%(lineno)d>%(name)s : %(message)s'
# with filename&lineno
FORMATTER_FULL4 = '[%(asctime)s](%(levelname)5s)<%(filename)s:%(lineno)d>%(name)s : %(message)s'
# the mini require
FORMATTER_MINI = '[%(asctime)s](%(levelname)5s)%(name)20s : %(message)s'

FORMATTER_ZL_PROJECT = '%(asctime)s [%(hostname)5s] [%(module)s] [%(threadName)s] %(levelname)5s [%(funcName)s] - %(message)s'


def check_file_path(full_file_path_name):
    """
    create file path if the path is not exists
    """
    file_path = os.path.dirname(full_file_path_name)
    if file_path and not os.path.exists(file_path):
        os.makedirs(file_path)


class ContextFilter(logging.Filter):
    def filter(self, record):
        import socket
        record.hostname = socket.gethostname()
        return True


class LoggerManager(object):
    @classmethod
    def init_logging(cls, log_file_name=None, log_level=logging.DEBUG, need_mail=False, need_console=False,
                     subject=None,
                     mail_list=None, need_rotating=True):
        '''

        :param log_file_name:  log file path  eg: /var/log/app.log
        :param log_level: log level default = logging.DEBUG
        :param need_mail:  是否需要邮件报警  需要配置 smtp setting
        :param need_console: print log record to console default: false
        :param subject: mail subject
        :param mail_list: mail receiver
        :param need_rotating: log 文件分割
        :return:
        '''
        logger_handler = None
        if log_file_name is not None and isinstance(log_file_name, str):
            check_file_path(log_file_name)
            if need_rotating:
                formatter = logging.Formatter(FORMATTER_ZL_PROJECT)
                logger_handler = TimedRotatingFileHandler(
                    log_file_name, when='D', interval=1, backupCount=10, encoding='utf8', delay=False, utc=False)
                logger_handler.setLevel(log_level)
                logger_handler.setFormatter(formatter)
                logger_handler.addFilter(ContextFilter())
                logging.getLogger().addHandler(logger_handler)
            else:
                logging.basicConfig(level=log_level, filename=log_file_name,
                                    format=FORMATTER_ZL_PROJECT,
                                    datefmt='%Y-%m-%d %H:%M:%S')
                logging.getLogger().addFilter(ContextFilter())
        if logger_handler is None or need_console is True:
            cls._append_console()
        if need_mail is True:
            mail_handler = cls._get_mail_handler(
                input_subject=subject, maillist=mail_list)
            logging.getLogger().addHandler(mail_handler)

    @classmethod
    def _append_console(cls, loglevel=logging.DEBUG):
        formatter = logging.Formatter(FORMATTER_ZL_PROJECT)
        consle_handler = logging.StreamHandler()
        consle_handler.setLevel(loglevel)
        consle_handler.setFormatter(formatter)
        logging.getLogger().addHandler(consle_handler)

    @classmethod
    def _get_mail_handler(cls, input_subject=None, maillist=None):
        formatter = logging.Formatter(FORMATTER_ZL_PROJECT)
        mail_host = 'smtp.host.com'
        from_addr = 'example@host.com'
        toaddrs = ['toaddrs@host.com']
        if maillist is not None and isinstance(maillist, list) and len(maillist) > 0:
            toaddrs = maillist
        subject = '[ERROR LOG]'
        if input_subject is not None:
            subject = input_subject
        credentials = ('example@host.com', 'password')
        mail_handler = SMTPHandler(
            mail_host, from_addr, toaddrs, subject, credentials=credentials, secure=None)
        mail_handler.setLevel(logging.ERROR)
        mail_handler.setFormatter(formatter)
        mail_handler.addFilter(ContextFilter())
        return mail_handler


def fn_timer(function):
    @wraps(function)
    def function_timer(*args, **kwargs):
        log = logging.getLogger()
        t0 = time.time()
        result = function(*args, **kwargs)
        t1 = time.time()
        log.debug("Total time running %s: %s seconds" %
                  (function.__name__, str(t1 - t0))
                  )
        return result

    return function_timer

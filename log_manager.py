import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
log_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s -%(message)s")
# 输出在console中
sh_handler = logging.StreamHandler()
sh_handler.setLevel(logging.INFO)
sh_handler.setFormatter(log_formatter)
logger.addHandler(sh_handler)



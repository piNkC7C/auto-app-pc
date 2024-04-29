import logging
from logging.handlers import TimedRotatingFileHandler
import queue
import os
from config.config import Configs


# def initLog():
#     logger = logging.getLogger("feiyang")
#     logger.setLevel(logging.DEBUG)
#     # 建立一个filehandler来把日志记录在文件里，级别为debug以上
#
#     # 创建一个handler，用于写入日志文件
#     # rq = time.strftime('%Y-%m-%d', time.localtime(time.time()))
#     # # log_date = rq[:10]
#     # log_path = os.getcwd() + '/Logs/'
#     # isExists = os.path.exists(log_path)
#     # # # 判断结果
#     # if not isExists:
#     #     os.makedirs(log_path)
#     # log_name = os.getcwd() + '/Logs/{}-'.format(rq) + '-info.log'
#     # fh = logging.FileHandler(log_name, mode="a")
#
#     fh = TimedRotatingFileHandler(filename="info.log", when="D", interval=1, backupCount=3)
#     fh.setLevel(logging.DEBUG)
#     # 建立一个streamhandler来把日志打在CMD窗口上，级别为error以上
#     ch = logging.StreamHandler()
#     ch.setLevel(logging.DEBUG)
#     # 设置日志格式
#     formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
#     ch.setFormatter(formatter)
#     fh.setFormatter(formatter)
#     # 将相应的handler添加在logger对象中
#     logger.addHandler(ch)
#     logger.addHandler(fh)

def initLog():
    # 创建队列
    log_queue = queue.Queue()

    # 创建并配置日志记录器
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # 获取数据目录
    config_data = Configs()
    directory = config_data.app_info['data_dir']

    # 创建"log"目录，如果不存在的话
    log_dir = f"{directory}\\logs"
    os.makedirs(log_dir, exist_ok=True)

    # 创建文件处理器
    file_handler = TimedRotatingFileHandler(filename=f"{log_dir}\\info.log",
                                            when="D",
                                            interval=1,
                                            backupCount=3, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)

    # 创建格式化器
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # 创建队列处理器
    queue_handler = logging.handlers.QueueHandler(log_queue)
    queue_handler.setLevel(logging.DEBUG)

    # 将队列处理器添加到日志记录器
    logger.addHandler(queue_handler)

    # 创建并启动队列监听器
    queue_listener = logging.handlers.QueueListener(log_queue, file_handler)
    queue_listener.start()


def debugLog(log):
    print(log)
    # 开始打日志
    logger = logging.getLogger(__name__)
    logger.debug(log)

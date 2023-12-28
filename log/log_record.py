import logging
from logging.handlers import TimedRotatingFileHandler

def initLog():
    logger = logging.getLogger("feiyang")
    logger.setLevel(logging.DEBUG)
    # 建立一个filehandler来把日志记录在文件里，级别为debug以上

    # 创建一个handler，用于写入日志文件
    # rq = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    # # log_date = rq[:10]
    # log_path = os.getcwd() + '/Logs/'
    # isExists = os.path.exists(log_path)
    # # # 判断结果
    # if not isExists:
    #     os.makedirs(log_path)
    # log_name = os.getcwd() + '/Logs/{}-'.format(rq) + '-info.log'
    # fh = logging.FileHandler(log_name, mode="a")

    fh = TimedRotatingFileHandler(filename="info.log", when="D", interval=1, backupCount=3)
    fh.setLevel(logging.DEBUG)
    # 建立一个streamhandler来把日志打在CMD窗口上，级别为error以上
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # 设置日志格式
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    # 将相应的handler添加在logger对象中
    logger.addHandler(ch)
    logger.addHandler(fh)
def debugLog(log):
    # 开始打日志
    logger = logging.getLogger("feiyang")
    logger.debug(log)

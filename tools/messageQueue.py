import pika
import json
import time
import socket
import asyncio
from datetime import datetime
from log.log_record import debugLog
from api.qwcosplayApi import qwcosplay_task_start, qwcosplay_task_finish, qwcosplay_task_interrupt, \
    qwcosplay_user_watch_status
from datetime import datetime
from config.config import Configs
from api.qwcosplayApi import qwcosplay_task_interrupt
from tools.tools import check_update


class MessageQueueManager:
    def __init__(self, deal_err, deal_noerr, deal_task):
        self.config_data = Configs()
        queue_config = self.config_data.queue_info
        self.hostname = queue_config["hostname"]
        self.port = queue_config["port"]
        self.username = queue_config["username"]
        self.password = queue_config["password"]
        # self.consumer_tag = []
        self.un_acked_task = []
        self.deal_err = deal_err
        self.deal_noerr = deal_noerr
        self.deal_task = deal_task
        self.connection = None
        self.channel = None
        self.tag = None
        self.network = 0

    def connect(self, con_time, wait_time, status, queue, userid, fei_num):
        try:
            credentials = pika.PlainCredentials(self.username, self.password)
            parameters = pika.ConnectionParameters(self.hostname, self.port, '/', credentials)
            self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()
            # if status == 1:
            #     self.deal_noerr()
            return True
        except Exception as e:
            # if con_time == 1 and status == 1:
            #     self.deal_err()
            # 这里处理其他类型的异常
            debugLog(f"连接队列出错：")
            debugLog(str(e))
            time.sleep(wait_time)
            return self.connect(con_time + 1, wait_time, status, queue, userid, fei_num)

    def insert_message_task(self, task, queue):
        try:
            if self.connect(1, 10, 0, queue, "", 1) is True:
                self.channel.queue_declare(queue=queue, durable=True)
                self.channel.basic_publish(
                    exchange='',
                    routing_key=queue,
                    body=json.dumps(task),
                    properties=pika.BasicProperties(
                        delivery_mode=2,  # make message persistent
                    )
                )
                debugLog("任务创建完成")
                self.close_connection()
        except Exception as e:
            debugLog("创建消息出错:")
            debugLog(str(e))

    def close_connection(self):
        try:
            if self.connection:
                debugLog("关闭连接")
                self.connection.close()
        except Exception as e:
            debugLog("关闭连接出错")
            debugLog(str(e))
        self.connection = None
        self.channel = None
        self.tag = None

    def consume_message_task(self, queue, userid, fei_num):
        try:
            if self.connect(1, 10, 1, queue, userid, fei_num) is True:
                self.channel.queue_declare(queue=queue, durable=True)
                self.channel.basic_qos(prefetch_count=1)

                def callback(ch, method, properties, body):
                    debugLog(f"{queue}收到任务")
                    is_deal_task = True
                    # task = body.decode('utf-8')
                    # debugLog("队列消息原型")
                    # debugLog(body)
                    task_json = json.loads(body.decode('utf-8'))
                    # task_json = json.loads(body.encode('utf-8').decode('unicode_escape'))
                    # time.sleep(10)
                    debugLog("任务详情")
                    debugLog(task_json)
                    # debugLog(fei_num)
                    if task_json['taskList'] == 'task':
                        ch.basic_ack(delivery_tag=method.delivery_tag)
                        check_update(self.config_data.app_name)
                        # is_deal_task = False
                        return
                    else:
                        if self.un_acked_task.__len__() != 0:
                            for index, task in enumerate(self.un_acked_task):
                                if task['id'] == task_json['id']:
                                    debugLog("该任务存在于非人为中断任务列表")
                                    asyncio.run(
                                        qwcosplay_task_interrupt(task_json['id'],
                                                                 datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                                                 f"任务ack出错：{task['err']}"))
                                    self.un_acked_task.pop(index)
                                    is_deal_task = False
                                    break
                    if is_deal_task:
                        self.deal_task(task_json, userid, fei_num)
                    try:
                        ch.basic_ack(delivery_tag=method.delivery_tag)
                        debugLog("任务完成")
                    except Exception as ack_error:
                        if 'ConnectionResetError' in ack_error.args[0]:
                            task_json = json.loads(body.decode('utf-8'))
                            self.un_acked_task.append({
                                "id": task_json['id'],
                                "err": ack_error
                            })
                        raise

                self.tag = self.channel.basic_consume(queue=queue, on_message_callback=callback)
                debugLog(f"队列tag：{self.tag}")
                debugLog(f"{queue}等待任务...")
                self.channel.start_consuming()
        except Exception as consume_err:
            debugLog("消费队列错误：")
            debugLog(str(consume_err))
            if 'ConnectionResetError' in consume_err.args[0]:
                debugLog("断网导致队列连接失败")
                # self.stop_consume_message_task(queue)
                # self.consume_message_task(queue, userid, fei_num)
                # self.close_connection()

    def stop_consume_message_task(self, queue):
        try:
            # if self.channel:
            #     debugLog(f"{queue}关闭消费...")
            #     res = self.channel.basic_cancel(self.tag)
            #     debugLog("关闭消费结果")
            #     debugLog(res)
            #     self.channel = None
            #     self.tag = None
            debugLog(f"{queue}关闭消费...")
            if self.channel:
                debugLog(f"tag：{self.tag}")
                self.channel.stop_consuming(self.tag)
                self.close_connection()
                # self.connection = None
                # self.channel = None
                # self.tag = None
                # res = self.channel.basic_cancel(self.tag)
                # debugLog("关闭消费结果")
                # debugLog(res)
                # self.tag = None
            # self.close_connection()
        except Exception as e:
            debugLog("停止消费队列出错:")
            debugLog(str(e))

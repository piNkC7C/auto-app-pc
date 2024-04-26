import pika
import json
import time
import asyncio
from datetime import datetime
from log.log_record import debugLog
from api.qwcosplayApi import qwcosplay_task_start, qwcosplay_task_finish, qwcosplay_task_interrupt, \
    qwcosplay_user_watch_status
from datetime import datetime
from config.config import Configs


class MessageQueueManager:
    def __init__(self):
        config_data = Configs()
        queue_config = config_data.queue_info
        self.hostname = queue_config["hostname"]
        self.port = queue_config["port"]
        self.username = queue_config["username"]
        self.password = queue_config["password"]
        self.consumer_tag = []

    def connect(self):
        credentials = pika.PlainCredentials(self.username, self.password)
        parameters = pika.ConnectionParameters(self.hostname, self.port, '/', credentials)
        return pika.BlockingConnection(parameters)

    def insert_message_task(self, task, queue, deal_err, deal_noerr):
        connection = None
        circle = True
        while circle:
            try:
                connection = self.connect()
            except Exception as e:
                deal_err()
                debugLog("连接消息队列时出错:")
                debugLog(str(e))
                # 释放之前的连接资源
                if connection:
                    connection.close()
                # 休眠一段时间后重试连接
                time.sleep(10)  # 休眠10秒后重试连接

            try:
                if connection:
                    circle = False
                    channel = connection.channel()
                    channel.queue_declare(queue=queue, durable=True)
                    channel.basic_publish(
                        exchange='',
                        routing_key=queue,
                        body=json.dumps(task),
                        properties=pika.BasicProperties(
                            delivery_mode=2,  # make message persistent
                        )
                    )
                    # deal_noerr()
                    debugLog("任务创建完成，关闭连接")
                    connection.close()
            except Exception as e:
                # circle = True
                # deal_err()
                debugLog("消息队列出错:")
                debugLog(str(e))
                # 释放之前的连接资源
                if connection:
                    connection.close()
                # 休眠一段时间后重试连接
                time.sleep(10)  # 休眠10秒后重试连接

    def consume_message_task(self, queue, deal_task, consume_state, deal_err, deal_noerr, userid):
        connection = None
        circle = True
        while circle:
            try:
                connection = self.connect()
            except Exception as e:
                deal_err()
                debugLog("连接消息队列时出错:")
                debugLog(str(e))
                # 释放之前的连接资源
                if connection:
                    connection.close()
                # 休眠一段时间后重试连接
                time.sleep(10)  # 休眠10秒后重试连接
                debugLog("尝试重新连接")

            try:
                if connection:
                    circle = False
                    channel = connection.channel()
                    channel.queue_declare(queue=queue, durable=True)
                    channel.basic_qos(prefetch_count=1)

                    def callback(ch, method, properties, body):
                        debugLog(f"{queue}收到任务")
                        try:
                            # task = body.decode('utf-8')
                            debugLog("队列消息原型")
                            debugLog(body)
                            task_json = json.loads(body.decode('utf-8'))
                            # task_json = json.loads(body.encode('utf-8').decode('unicode_escape'))
                            debugLog(task_json)
                            deal_task(task_json, userid)
                        except Exception as deal_task_error:
                            # deal_err()
                            debugLog("处理队列任务时出错:")
                            debugLog(str(deal_task_error))

                        ch.basic_ack(delivery_tag=method.delivery_tag)

                    tag = channel.basic_consume(queue=queue, on_message_callback=callback)
                    debugLog(f"队列tag：{tag}")
                    index = next((i for i, obj in enumerate(self.consumer_tag) if getattr(obj, 'queue', None) == queue),
                                 None)
                    # if index is None:
                    self.consumer_tag.append({
                        "queue": queue,
                        "connection": connection,
                        "channel": channel,
                        "consumer_tag": tag,
                    })
                    # deal_noerr()
                    debugLog(f"{queue}等待任务...")
                    try:
                        channel.start_consuming()
                    except Exception as e:
                        debugLog(str(e))
            except Exception as e:
                # circle = True
                # deal_err()
                debugLog("消息队列出错:")
                debugLog(str(e))
                # 释放之前的连接资源
                if connection:
                    connection.close()
                # 休眠一段时间后重试连接
                time.sleep(10)  # 休眠10秒后重试连接

    def stop_consume_message_task(self, queue):
        try:
            # debugLog(queue)
            # debugLog(self.consumer_tag)
            if self.consumer_tag.__len__() != 0:
                for index, tag in enumerate(self.consumer_tag):
                    if tag["queue"] == queue:
                        debugLog(f"{queue}关闭消费...")
                        tag["channel"].basic_cancel(tag["consumer_tag"])
                        # tag["connection"].close()
                        # 关闭连接
                        self.consumer_tag.pop(index)
                        debugLog(f"删除队列tag：{tag['consumer_tag']}")
        except Exception as e:
            debugLog("停止消费队列时出错:")
            debugLog(str(e))

    def delete_message_task(self, queue):
        connection = self.connect()
        channel = connection.channel()
        channel.queue_delete(queue=queue)
        debugLog(f"队列 {queue} 已成功删除")
        connection.close()

import pika
import json
from datetime import datetime
from tools.fileOperate import File


class MessageQueueManager:
    def __init__(self):
        file_manager = File()
        queue_config = file_manager.get_file_data("assets/queue.json")
        self.hostname = queue_config["hostname"]
        self.port = queue_config["port"]
        self.username = queue_config["username"]
        self.password = queue_config["password"]
        self.consumer_tag = []

    def connect(self):
        credentials = pika.PlainCredentials(self.username, self.password)
        parameters = pika.ConnectionParameters(self.hostname, self.port, '/', credentials)
        return pika.BlockingConnection(parameters)

    def insert_message_task(self, task, queue):
        connection = self.connect()
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
        print("任务创建完成，关闭连接")
        connection.close()

    def consume_message_task(self, queue, deal_task, consume_state):
        connection = self.connect()
        channel = connection.channel()
        # channel.queue_declare(queue=queue, durable=True)
        channel.basic_qos(prefetch_count=1)

        def callback(ch, method, properties, body):
            print(f"{queue}收到任务")
            # task = body.decode('utf-8')
            task = json.loads(body.decode('utf-8'))
            deal_task(task)
            ch.basic_ack(delivery_tag=method.delivery_tag)

        tag = channel.basic_consume(queue=queue, on_message_callback=callback)
        print(tag)
        index = next((i for i, obj in enumerate(self.consumer_tag) if getattr(obj, 'queue', None) == queue), None)
        print(index)
        # if index is None:
        self.consumer_tag.append({
            "queue": queue,
            "connection": connection,
            "channel": channel,
            "consumer_tag": tag,
        })
        print(f"{queue}等待任务...")
        channel.start_consuming()

    def stop_consume_message_task(self, queue):
        print(queue)
        print(self.consumer_tag)
        for index, tag in enumerate(self.consumer_tag):
            if tag["queue"] == queue:
                print(f"{queue}关闭消费...")
                tag["channel"].basic_cancel(tag["consumer_tag"])
                # 关闭连接
                # tag["connection"].close()
                self.consumer_tag.pop(index)
                print(self.consumer_tag)

    def delete_message_task(self, queue):
        connection = self.connect()
        channel = connection.channel()
        channel.queue_delete(queue=queue)
        print(f"队列 {queue} 已成功删除")
        connection.close()

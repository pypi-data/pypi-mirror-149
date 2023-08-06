import logging
import sys
from queue import Queue
from threading import Thread
import pika


class Consumer:
    def __init__(self, config: dict, msg_queue: Queue):
        self.msg_queue = msg_queue
        rabbitmq_config = {"leaf_name": "",
                           "leaf_id": "",
                           "queue_password": "",
                           "host": "response.branchkey.com",
                           "port": 5672,
                           "branch_id": "",
                           "tree_id": "",
                           "heartbeat_time_s": 30,
                           "conn_retries": 3,
                           "conn_retry_delay_s": 3}

        for key in config:
            rabbitmq_config[key] = config[key]

        self.queue_name = rabbitmq_config['leaf_id']

        self.rabbitmq_config = rabbitmq_config

        self.conn = self.__get_connection()
        self.channel = self.conn.channel()
        self.exchange = self.rabbitmq_config['branch_id']

    def __get_connection(self):
        try:
            creds = pika.PlainCredentials(
                self.rabbitmq_config["leaf_id"], self.rabbitmq_config["queue_password"])

            conn = pika.BlockingConnection(pika.ConnectionParameters(
                host=self.rabbitmq_config["host"],
                port=self.rabbitmq_config["port"],
                virtual_host=self.rabbitmq_config['tree_id'],
                credentials=creds,
                heartbeat=int(self.rabbitmq_config["heartbeat_time_s"]),
                connection_attempts=int(self.rabbitmq_config["conn_retries"]),
                retry_delay=int(self.rabbitmq_config["conn_retry_delay_s"])
            ))

        except Exception as e:
            sys.exit("[Consumer] Error while connecting to rabbitmq: " + str(e))

        else:
            return conn

    def __callback(self, ch, method, properties, body):
        msg = body.decode()
        logging.info("[Consumer] Message received: " + msg)

        self.msg_queue.put(msg, block=False)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def start(self):
        self.channel.basic_consume(
            queue=self.queue_name, on_message_callback=self.__callback)
        try:
            logging.info("[Consumer] Starting rabbitmq consumer")
            self.channel.start_consuming()

        except Exception as e:
            self.stop()

    def stop(self, err=None):
        logging.info("[Consumer] Stopping rabbitmq consumer: " + str(err))
        if self.channel.is_open:
            self.channel.close()
        if self.conn.is_open:
            self.conn.close()

    def spawn_consumer_thread(self):
        t = ConsumerThread(target=self.start, callback=self.stop, daemon=True)
        t.start()
        return t


class ConsumerThread(Thread):
    def __init__(self, callback=None, *args, **keywords):
        Thread.__init__(self, *args, **keywords)
        self.callback = callback
        self.killed = False

    def start(self):
        self.__run_backup = self.run
        self.run = self.__run
        Thread.start(self)

    def __run(self):
        sys.settrace(self.globaltrace)
        self.__run_backup()
        self.run = self.__run_backup

    def globaltrace(self, frame, event, arg):
        if event == 'call':
            return self.localtrace
        else:
            return None

    def localtrace(self, frame, event, arg):
        if self.killed:
            if event == 'line':
                raise SystemExit()
        return self.localtrace

    def kill(self):
        # self.callback()
        self.killed = True

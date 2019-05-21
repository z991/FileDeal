import os
import traceback
import logging
import asyncio
import aiomysql
import threading


from database.database import DataBase
from config.settings import db_config
from modules.fileread import FileRead
from config.settings import push_url
import uvloop


class HandlerCenter(object):

    def __init__(self, master_queue):
        self.master_queue = master_queue
        self.loop = None
        self.db = ""

    def execute(self):
        try:
            while True:
                message = self.master_queue.get()
                # 将调度一个协程到在另一个线程中运行的事件循环，但它返回一个 concurrent.futures.Future 对象
                asyncio.run_coroutine_threadsafe(self.handle_message(message), loop=self.loop)
        except Exception as e:
            exec = traceback.format_exc()
            logging.error(exec)

    async def handle_message(self, message):
        file_read = FileRead(self.loop, self.db, push_url)
        await file_read.execute(message)

    async def app_factory(self):
        try:
            pool = await aiomysql.create_pool(host=db_config["host"], port=int(db_config["port"]), user=db_config["user"], password=db_config["password"], db=db_config["db"], minsize=int(db_config["minsize"]), maxsize=int(db_config["maxsize"]), loop=self.loop, autocommit=True, pool_recycle=7*3600)
            self.db = DataBase(pool)
        except Exception as e:
            logging.error(e)

    def start_coroutine(self):
        """
        创建协程
        :return:
        """
        try:
            # self.loop = asyncio.new_event_loop()
            # asyncio.set_event_loop(self.loop)
            self.loop = uvloop.new_event_loop()
            self.loop.create_task(self.app_factory())
            self.loop.run_forever()
        except Exception as e:
            logging.error(e)

    @classmethod
    def run(cls, master_queue):
        handler_center = cls(master_queue)
        
        # 启动协程
        coroutine_thread = threading.Thread(
            target=handler_center.start_coroutine)
        coroutine_thread.start()

        handler_center.execute()
        


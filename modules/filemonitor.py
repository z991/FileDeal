from watchdog.events import FileSystemEventHandler
import logging
import time

class FileMonitor(FileSystemEventHandler):

    def __init__(self, callback):
        self.callback = callback

    def on_moved(self, event):
        super(FileMonitor, self).on_moved(event)
        what = 'directory' if event.is_directory else 'file'
        print('what===move', what)
        # 后面用到可以添加对应的回调

    def on_deleted(self, event):
        super(FileMonitor, self).on_deleted(event)
        what = 'directory' if event.is_directory else 'file'
        # 后面用到可以添加对应的回调

    def on_modified(self, event):
        super(FileMonitor, self).on_modified(event)
        what = 'directory' if event.is_directory else 'file'
        print('what===modifi', what)
        # 后面用到可以添加对应的回调
        
    def on_created(self, event):
        super(FileMonitor, self).on_moved(event)
        what = 'directory' if event.is_directory else 'file'
        logging.info("{0} Created : {1} ".format(what, event.src_path))
        self.callback(event.src_path)

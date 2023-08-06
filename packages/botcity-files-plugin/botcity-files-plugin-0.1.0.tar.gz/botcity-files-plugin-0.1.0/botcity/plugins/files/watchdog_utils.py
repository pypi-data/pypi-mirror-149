import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class Handler(FileSystemEventHandler):

    def __init__(self, file_extension: str):
        self.file_extension = file_extension
        self.found_file = None

    def on_any_event(self, event):
        if event.event_type == "created" or event.event_type == "modified":
            if not event.is_directory:
                if self.file_extension:
                    file, ext = os.path.splitext(event.src_path)
                    if str(ext) == self.file_extension:
                        self.found_file = str(event.src_path)
                else:
                    self.found_file = str(event.src_path)


class Watcher:
    def __init__(self, directory: str, timeout: int, handler: Handler):
        self.observer = Observer()
        self.handler = handler
        self.directory = directory
        self.timeout = timeout

    def run(self):
        self.observer.schedule(self.handler, self.directory)
        self.observer.start()

        try:
            start_time = time.time()
            while True:
                elapsed_time = (time.time() - start_time) * 1000
                if elapsed_time > self.timeout:
                    break
                if self.handler.found_file:
                    break
                time.sleep(1)
        finally:
            self.observer.stop()
            self.observer.join()

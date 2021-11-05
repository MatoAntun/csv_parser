import os
import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, FileSystemEventHandler
from process import CsvProcessing
from datetime import datetime

class CreatedHandler(FileSystemEventHandler):

    def __init__(self):
        pass

    def process(self, filename):
        start = datetime.now()
        print(CsvProcessing(filename).read_csv())
        print("Time needed for basic", datetime.now() - start)

        # start = datetime.now()
        # print(CsvProcessing(filename).read_csv_single_threaded())
        # print("Time needed single threaded", datetime.now() - start)

        # start = datetime.now()
        # print(CsvProcessing(filename).read_csv_threads())
        # print("Time needed threded", datetime.now() - start)

        # start = datetime.now()
        # print(CsvProcessing(filename).read_csv_processes())
        # print("Time needed processes", datetime.now() - start)

    def on_created(self, event):
        if event.is_directory:
            return
        _, ext = os.path.splitext(event.src_path)
        print(f"Created file {event.src_path}")
        # trenutno samo da vidimo koliko overhead moramo dati
        if (ext == '.csv'):
            lines = list()
            with open(event.src_path, 'r') as f:
                lines = f.readlines()
            print(len(lines))
        self.process(event.src_path)
        return event.src_path

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    event_handler = CreatedHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.deamon = True
    observer.start()
    try:
        while True:
            time.sleep(20)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

    if observer.is_alive():
       print('still alive')
    else:
        print('thread ending') 
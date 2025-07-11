import sys
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os

class ReloadHandler(FileSystemEventHandler):
    def __init__(self, script):
        self.script = script
        self.process = None
        self.start_process()

    def start_process(self):
        if self.process:
            self.process.terminate()
        self.process = subprocess.Popen([sys.executable, self.script])

    def on_modified(self, event):
        if event.src_path.endswith('.py'):
            print(f"{event.src_path} changed, restarting...")
            self.start_process()

if __name__ == "__main__":
    script = "main_page.py"  # 실행할 파일 경로
    event_handler = ReloadHandler(script)
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(script) or ".", recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    if event_handler.process:
        event_handler.process.terminate()
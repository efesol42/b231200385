import json
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Log dosyasının yolu
log_file_path = '/home/kali/bsm/logs/changes.json'

class FileChangeHandler(FileSystemEventHandler):
    def on_created(self, event):
        self.log_change(event)

    def on_deleted(self, event):
        self.log_change(event)

    def on_modified(self, event):
        self.log_change(event)

    def on_moved(self, event):
        self.log_change(event)

    def log_change(self, event):
        # Değişiklik bilgilerini JSON formatında kaydet
        change_info = {
            'event_type': event.event_type,  # 'created', 'modified', 'deleted', 'moved'
            'src_path': event.src_path,
            'timestamp': time.time()
        }

        # Log dosyasını güncelle
        if os.path.exists(log_file_path):
            with open(log_file_path, 'r') as log_file:
                logs = json.load(log_file)
        else:
            logs = []

        logs.append(change_info)

        with open(log_file_path, 'w') as log_file:
            json.dump(logs, log_file, indent=4)

if _name_ == "_main_":
    # İzlenecek dizin
    directory_to_watch = '/home/kali/bsm/test'

    # Handler ve Observer'ı başlat
    event_handler = FileChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, directory_to_watch, recursive=True)

    try:
        observer.start()
        print(f"test dosyası izleniyor...")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

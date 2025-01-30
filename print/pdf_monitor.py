import os
import time
import shutil
import win32api
import win32print
import configparser
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def load_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return (
        os.path.abspath(config['DEFAULT']['monitoring_path']),
        config['DEFAULT']['printer_name']
    )

class PDFHandler(FileSystemEventHandler):
    def __init__(self, monitoring_path, printer_name):
        self.monitoring_path = monitoring_path
        self.printer_name = printer_name
        self.printed_dir = os.path.join(monitoring_path, 'printed')
        os.makedirs(self.printed_dir, exist_ok=True)

    def on_created(self, event):
        if not event.is_directory and event.src_path.lower().endswith('.pdf'):
            time.sleep(1)  # Allow file to be fully written
            self.process_file(event.src_path)

    def process_file(self, file_path):
        try:
            # Print the PDF
            win32api.ShellExecute(
                0,
                "print",
                file_path,
                f'/d:"{self.printer_name}"',
                ".",
                0
            )
            print(f"Sent to printer: {os.path.basename(file_path)}")
            
            # Move to printed directory
            #dest = os.path.join(self.printed_dir, os.path.basename(file_path))
            #shutil.move(file_path, dest)
            #print(f"Moved to printed folder: {dest}")
            
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")

def main():
    monitoring_path, printer_name = load_config()
    
    if not os.path.exists(monitoring_path):
        os.makedirs(monitoring_path)
        print(f"Created monitoring directory: {monitoring_path}")

    event_handler = PDFHandler(monitoring_path, printer_name)
    observer = Observer()
    observer.schedule(event_handler, monitoring_path, recursive=False)
    observer.start()

    print(f"Monitoring: {monitoring_path}")
    print(f"Printer: {printer_name}")
    print("Press Ctrl+C to exit")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
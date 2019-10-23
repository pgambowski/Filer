from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path
import os
import time
import platform
import getpass


def create_directories():
    paths = ["Documents", "Images", "Video", "Music", "Other"]
    for item in paths:
        path = Path("{}/{}".format(desktop_path, item))
        if not os.path.exists(path):
            os.mkdir(path)
            print('Directory "{}" has been created.'.format(path))
        else:
            print('Directory "{}" already exists.'.format(path))


def get_destination_directory_name(ext):
    print('File extention is: "{}"'.format(ext))
    return{
        '.jpg': 'Images',
        '.jpeg': 'Images',
        '.png': 'Images',
        '.gif': 'Images',
        '.txt': 'Documents',
        '.doc': 'Documents',
        '.docx': 'Documents',
        '.pdf': 'Documents',
        '.html': 'Documents',
        '.ppt': 'Documents',
        '.xlsx': 'Documents',
        '.mp3': 'Music',
        '.wav': 'Music',
        '.mp4': 'Video',
    }.get(ext, 'Other')


class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print("Folder has been modified: filename: {}.".format(event.src_path))
        for filename in os.listdir(downloads_folder):
            ext = os.path.splitext(filename)[-1].lower()
            if filename == 'desktop.ini' or ext == '.tmp':
                continue
            src = Path("{}/{}".format(downloads_folder, filename))
            time.sleep(5)
            dst = Path("{}/{}/{}".format(desktop_path, get_destination_directory_name(ext), filename))
            print('moving "{}" from "{}" to "{}"'.format(filename, downloads_folder, dst))
            os.rename(src, dst)


if platform.system() == "Windows":
    downloads_folder = r"C:\Users\{}\Downloads".format(getpass.getuser())
    desktop_path = r"C:\Users\{}\Desktop".format(getpass.getuser())
elif platform.system() == "Linux":
    downloads_folder = '/home/{}/Downloads'.format(getpass.getuser())
    desktop_path = '~/Desktop'
else:
    print("Sorry your operating system is not supported")

create_directories()
event_handler = MyHandler()
observer = Observer()
observer.schedule(event_handler, downloads_folder, recursive=True)
observer.start()
try:
    while True:
        time.sleep(5)
except KeyboardInterrupt:
    observer.stop()
observer.join()

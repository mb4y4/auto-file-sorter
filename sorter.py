import os
import time
import logging
from logging.handlers import RotatingFileHandler
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from dotenv import load_dotenv

# Load configuration from .env
load_dotenv()

WATCH_DIR = os.getenv("WATCH_DIR", os.path.expanduser("~/Downloads"))
LOG_DIR = os.getenv("LOG_DIR", "logs")

# Ensure log directory exists
os.makedirs(LOG_DIR, exist_ok=True)

# Setup logging with rotation (5 logs, 1MB each)
log_file = os.path.join(LOG_DIR, "file_sorter.log")
logger = logging.getLogger("FileSorter")
logger.setLevel(logging.INFO)

handler = RotatingFileHandler(log_file, maxBytes=1_000_000, backupCount=5)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

# Avoid duplicate handlers when script restarts
if not logger.handlers:
    logger.addHandler(handler)

# File categories based on extension
FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".xls", ".xlsx", ".ppt", ".pptx"],
    "Audio": [".mp3", ".wav", ".aac", ".flac"],
    "Videos": [".mp4", ".avi", ".mov", ".mkv"],
    "Archives": [".zip", ".rar", ".tar", ".gz", ".7z"],
    "Scripts": [".py", ".js", ".sh", ".bat", ".java", ".cpp", ".go"],
}

class FileSorterHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            self.sort_file(event.src_path)

    def sort_file(self, file_path):
        file_ext = os.path.splitext(file_path)[1].lower()
        moved = False

        for category, extensions in FILE_TYPES.items():
            if file_ext in extensions:
                category_path = os.path.join(WATCH_DIR, category)
                os.makedirs(category_path, exist_ok=True)
                new_path = os.path.join(category_path, os.path.basename(file_path))
                
                try:
                    os.rename(file_path, new_path)
                    logger.info(f"Moved: {file_path} -> {new_path}")
                except Exception as e:
                    logger.error(f"Error moving {file_path}: {e}")
                moved = True
                break

        if not moved:
            other_path = os.path.join(WATCH_DIR, "Others")
            os.makedirs(other_path, exist_ok=True)
            new_path = os.path.join(other_path, os.path.basename(file_path))
            try:
                os.rename(file_path, new_path)
                logger.info(f"Moved: {file_path} -> {new_path}")
            except Exception as e:
                logger.error(f"Error moving {file_path}: {e}")

def start_sorting():
    logger.info(f"🚀 Auto File Sorter started on {WATCH_DIR}")
    event_handler = FileSorterHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_DIR, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        logger.info("🛑 File Sorter stopped manually")
    observer.join()

if __name__ == "__main__":
    start_sorting()

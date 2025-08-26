import os
import shutil
import time
import argparse
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# --- Configuration ---
DOWNLOADS_DIR = os.path.expanduser("~/Downloads")
DEST_DIRS = {
    "images": os.path.expanduser("~/Downloads/Sorted/Images"),
    "pdfs": os.path.expanduser("~/Downloads/Sorted/PDFs"),
    "docs": os.path.expanduser("~/Downloads/Sorted/Documents"),
    "others": os.path.expanduser("~/Downloads/Sorted/Others")
}

# Create destination folders if not exist
for path in DEST_DIRS.values():
    os.makedirs(path, exist_ok=True)


def sort_file(file_path):
    """Move file based on extension."""
    if not os.path.isfile(file_path):
        return

    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    if ext in [".jpg", ".jpeg", ".png", ".gif"]:
        target_dir = DEST_DIRS["images"]
    elif ext in [".pdf"]:
        target_dir = DEST_DIRS["pdfs"]
    elif ext in [".docx", ".doc", ".txt"]:
        target_dir = DEST_DIRS["docs"]
    else:
        target_dir = DEST_DIRS["others"]

    try:
        shutil.move(file_path, target_dir)
        print(f"Moved {file_path} → {target_dir}")
    except Exception as e:
        print(f"Error moving {file_path}: {e}")


def manual_sort():
    """Sort all existing files in Downloads once."""
    for file in os.listdir(DOWNLOADS_DIR):
        file_path = os.path.join(DOWNLOADS_DIR, file)
        if os.path.isfile(file_path):
            sort_file(file_path)


class Watcher(FileSystemEventHandler):
    """Realtime monitor class for watchdog."""

    def on_created(self, event):
        if not event.is_directory:
            sort_file(event.src_path)


def realtime_sort():
    """Keep watching Downloads folder in realtime."""
    event_handler = Watcher()
    observer = Observer()
    observer.schedule(event_handler, DOWNLOADS_DIR, recursive=False)
    observer.start()
    print("Watching for new files in Downloads... (Ctrl+C to stop)")
    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["manual", "realtime"], default="manual")
    args = parser.parse_args()

    if args.mode == "manual":
        manual_sort()
    else:
        realtime_sort()

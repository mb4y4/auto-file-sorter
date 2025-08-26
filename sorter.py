import os
import sys
import time
import shutil
import logging
from logging.handlers import RotatingFileHandler

# ---- Fallback fix for Windows/Pylance not resolving python-dotenv ----
try:
    from dotenv import load_dotenv
except ImportError:
    sys.path.append(
        os.path.expanduser("~\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\site-packages")
    )
    from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- Logging setup with rotation ---
log_handler = RotatingFileHandler(
    "file_sorter.log", maxBytes=1_000_000, backupCount=5
)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[log_handler]
)

# --- Get configuration from .env ---
WATCH_DIR = os.getenv("WATCH_DIR", "./watch_folder")
SORTED_DIR = os.getenv("SORTED_DIR", "./sorted_folder")

# File type mapping
FILE_TYPES = {
    "images": [".jpg", ".jpeg", ".png", ".gif"],
    "documents": [".pdf", ".docx", ".txt"],
    "videos": [".mp4", ".mov", ".avi"],
    "archives": [".zip", ".rar", ".tar", ".gz"],
}


def create_folders():
    """Ensure target folders exist for each category"""
    for folder in FILE_TYPES.keys():
        os.makedirs(os.path.join(SORTED_DIR, folder), exist_ok=True)


def sort_files():
    """Move files into categorized folders"""
    for filename in os.listdir(WATCH_DIR):
        file_path = os.path.join(WATCH_DIR, filename)
        if os.path.isfile(file_path):
            moved = False
            for folder, extensions in FILE_TYPES.items():
                if any(filename.lower().endswith(ext) for ext in extensions):
                    dest = os.path.join(SORTED_DIR, folder, filename)
                    shutil.move(file_path, dest)
                    logging.info(f"Moved {filename} → {folder}")
                    moved = True
                    break
            if not moved:
                dest = os.path.join(SORTED_DIR, "others")
                os.makedirs(dest, exist_ok=True)
                shutil.move(file_path, os.path.join(dest, filename))
                logging.info(f"Moved {filename} → others")


def main():
    create_folders()
    logging.info("Started monitoring...")
    try:
        while True:
            sort_files()
            time.sleep(5)  # check every 5 seconds
    except KeyboardInterrupt:
        logging.info("Stopped by user.")


if __name__ == "__main__":
    main()

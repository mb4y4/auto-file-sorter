# 🗂️ Auto File Sorter

A real-time file organizer that automatically sorts files into folders based on their extensions.  
It runs in the background and rotates logs to keep track of all file moves.

---

## 🚀 Features
- Monitors a folder in **real-time**.
- Automatically sorts files into categories (Images, Documents, Music, Videos, Archives, Others).
- Uses `.env` file for configurable **WATCH_FOLDER**.
- **Rotating logs** → keeps max 5 logs of 1MB each.
- Lightweight and runs in the background.

---

## 📦 Requirements
- Python 3.8+
- Packages from `requirements.txt`:
  ```bash
  pip install -r requirements.txt
## ⚙️ Setup & Usage
1. Clone this Repository;
   ```bash
   git clone https://github.com/YOUR_USERNAME/auto-file-sorter.git
   cd auto-file-sorter
2. Create a `.env` file in the project root:
   ```bash
   env
   
   WATCH_FOLDER=/path/to/watch
  Example (Windows):
    ```bash
  
    WATCH_FOLDER=F:/Downloads
3. Run the setup script:
    ```bash
    ./setup_and_run.sh
  Or run manually:
    ```bash
    python sorter.py

## 📝 Logging
- Logs are saved in `logs/sorter.log`.
- Log rotation is enabled (max 5 logs of 1MB each).

## 🔄 Customization
- Edit `sorter.py` to add new file categories or change folder rules.
- Example: Add `.csv` to the Documents category.

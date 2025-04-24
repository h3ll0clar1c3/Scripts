import os
import shutil
import time
from datetime import datetime

# Configuration
SOURCE_DIR = "/path/to/source"  # Path to the folder you want to back up
BACKUP_DIR = "/path/to/backup"  # Path where the backup will be stored
BACKUP_RETENTION_DAYS = 7       # Number of days to keep old backups

def create_backup(source, destination):
    """Creates a timestamped backup."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(destination, f"backup_{timestamp}")
    
    try:
        shutil.copytree(source, backup_path)
        print(f"Backup created successfully at {backup_path}")
    except Exception as e:
        print(f"Error creating backup: {e}")

def cleanup_old_backups(destination, retention_days):
    """Removes backups older than the retention period."""
    now = time.time()
    for folder in os.listdir(destination):
        folder_path = os.path.join(destination, folder)
        if os.path.isdir(folder_path):
            folder_age = now - os.path.getmtime(folder_path)
            if folder_age > retention_days * 86400:  # Convert days to seconds
                try:
                    shutil.rmtree(folder_path)
                    print(f"Deleted old backup: {folder_path}")
                except Exception as e:
                    print(f"Error deleting backup {folder_path}: {e}")

def main():
    # Ensure the backup directory exists
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

    # Create a new backup
    create_backup(SOURCE_DIR, BACKUP_DIR)

    # Cleanup old backups
    cleanup_old_backups(BACKUP_DIR, BACKUP_RETENTION_DAYS)

if __name__ == "__main__":
    main()

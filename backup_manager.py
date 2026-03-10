import sys
import shutil
from pathlib import Path
from datetime import datetime

# Accept source and backup directory from command-line arguments
if len(sys.argv) != 3:
    print("Usage: python backup_manager.py <source_directory> <backup_directory>")
    sys.exit(1)

source_dir = Path(sys.argv[1])
backup_dir = Path(sys.argv[2])

# Check if source exists
if not source_dir.exists():
    print(f"Source directory '{source_dir}' does not exist.")
    sys.exit(1)

# Create backup directory if it doesn't exist
backup_dir.mkdir(parents=True, exist_ok=True)

# Extensions we want to back up
target_extensions = {".csv", ".json"}

# Timestamp for this backup run
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# Open log file in append mode
log_file = open("backup_log.txt", "a")

def log(message):
    """Write message to both console and log file."""
    print(message)
    log_file.write(message + "\n")

log(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] --- Backup started ---")
log(f"Source: {source_dir}")
log(f"Destination: {backup_dir}")

# Loop through all files in source directory
for file_path in source_dir.iterdir():
    if file_path.is_file() and file_path.suffix in target_extensions:
        # Build new filename with timestamp
        stem = file_path.stem
        ext = file_path.suffix
        new_name = f"{stem}_{timestamp}{ext}"
        dest_path = backup_dir / new_name

        # Copy the file
        shutil.copy2(file_path, dest_path)
        log(f"Copied: {file_path.name} -> {new_name}")

        # --- Rotation: Keep only last 5 backups per original file ---
        # Find all backups of this original file
        pattern = f"{stem}_*{ext}"
        existing_backups = sorted(backup_dir.glob(pattern))

        # If more than 5, delete the oldest ones
        if len(existing_backups) > 5:
            to_delete = existing_backups[:-5]  # all but last 5
            for old_file in to_delete:
                old_file.unlink()
                log(f"Deleted old backup: {old_file.name}")

log(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] --- Backup completed ---")
log_file.close()

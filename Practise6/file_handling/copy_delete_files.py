import shutil
import os

source_file = "sample.txt"
backup_file = "sample_backup.txt"
# 4
  
if os.path.exists(source_file):
    shutil.copy(source_file, backup_file)
    print(f"Backup successful! Created: '{backup_file}'")
else:
    print(f"Source file '{source_file}' not found. Cannot create backup.")

#5
file_to_remove = "sample.txt"

if os.path.exists(file_to_remove):
    os.remove(file_to_remove)
    print(f"File '{file_to_remove}' has been safely deleted.")
else:
    print(f"Deletion failed: '{file_to_remove}' does not exist.")
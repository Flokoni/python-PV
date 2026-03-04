import os
import shutil

source_file = "move_me.txt"
destination_dir = "destination_folder"

with open(source_file, "w") as f:
    f.write("File to be moved")

if not os.path.exists(destination_dir):
    os.makedirs(destination_dir)

# 4
destination_path = os.path.join(destination_dir, source_file)

if os.path.exists(source_file):
    shutil.move(source_file, destination_path)
    print(f"File moved to: {destination_path}")
else:
    print("Source file not found, maybe it was already moved?")
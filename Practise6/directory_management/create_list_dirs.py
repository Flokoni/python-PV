import os

nested_path = "root_folder/sub_folder/target_folder"

if not os.path.exists(nested_path):
    os.makedirs(nested_path)
    print(f"Directories created: {nested_path}")
else:
    print("Directories already exist.")

# 2
current_dir = "."
print(f"Contents of '{current_dir}':")
for item in os.listdir(current_dir):
    print(f"- {item}")

# 3 
extension = ".py"
print(f"Searching for {extension} files:")
for file in os.listdir(current_dir):
    if file.endswith(extension):
        print(f"Found Python file: {file}")
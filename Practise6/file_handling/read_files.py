#2
filename = "sample.txt"

print(f"Reading content from {filename}...")

try:
    with open(filename, "r", encoding="utf-8") as file:
        content = file.read()
        print(" File Content Start ")
        print(content)
        print(" File Content End ")
except FileNotFoundError:
    print(f"Error: The file '{filename}' does not exist. Please run write_files.py first.")
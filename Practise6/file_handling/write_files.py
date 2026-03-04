#1
filename = "sample.txt"

with open(filename, "w", encoding="utf-8") as file:
    file.write("Line 1: Initial data\n")
    file.write("Line 2: Initial data\n")

print(f"File '{filename}' has been created and initial data was written.")

#3 Append new lin
with open(filename, "a", encoding="utf-8") as file:
    file.write("Line 3: Appended data\n")
    file.write("Line 4: Appended data\n")

print("New lines successfully added to the file.")
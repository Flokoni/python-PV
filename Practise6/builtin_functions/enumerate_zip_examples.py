#  3

names = ["Alice", "Bob", "Charlie"]
scores = [85, 92, 78]


print("--- Using enumerate ---")
for index, name in enumerate(names, start=1):
    print(f"Student #{index}: {name}")

print("\n--- Using zip ---")
for name, score in zip(names, scores):
    print(f"{name} scored {score} points")

items = [10, "Python", 3.14]
for item in items:
    print(f"Item: {item}, Type: {type(item)}")
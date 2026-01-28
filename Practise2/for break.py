for i in range(10):
    if i == 5: break
    print(i)

fruits = ["apple", "banana", "cherry", "date"]
for x in fruits:
    if x == "cherry": break
    print(x)

numbers = [10, 20, -5, 30, 40]
for n in numbers:
    if n < 0: break
    print(n)

for char in "Python":
    if char == "h": break
    print(char)

data = [1, 3, 5, 8, 9, 10]
for num in data:
    if num % 2 == 0:
        print("First even found:", num)
        break


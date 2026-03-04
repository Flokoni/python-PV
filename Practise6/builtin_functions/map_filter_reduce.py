from functools import reduce

numbers = [1, 2, 3, 4, 5, 6]

#  1
squares = list(map(lambda x: x**2, numbers))
evens = list(filter(lambda x: x % 2 == 0, numbers))

print(f"Original: {numbers}")
print(f"Squares (map): {squares}")
print(f"Evens (filter): {evens}")

#  2
total_sum = reduce(lambda x, y: x + y, numbers)
print(f"Total sum (reduce): {total_sum}")

#  4
value = "100"
if isinstance(value, str):
    converted_value = int(value)
    print(f"Converted '{value}' from {type(value)} to {type(converted_value)}")
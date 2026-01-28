i = 0
while i < 5:
    i += 1
    if i == 3: continue
    print(i)

n = 0
while n < 6:
    n += 1
    if n % 2 == 0: continue
    print(n)

x = 10
while x > 0:
    x -= 1
    if x == 7: continue
    print("Value:", x)

count = 0
while count < 4:
    count += 1
    if count < 3: continue
    print("Last items:", count)

step = 0
while step < 5:
    step += 1
    if step == 1 or step == 4: continue
    print("Step:", step)
input = "chethan_.123"
length = len(input)
count = 0
for char in input:
    if char.isdigit():
        count += 1
print("Number of digits:", count)
print(length)
r
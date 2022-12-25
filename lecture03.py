line = [True, True, False, False, True, True]

print(len(line))

for item in line:
    print(item)

print(line[0])
print(line[1])

###

if True:
    print("yes")
else:
    print("no")

if line[0]:
    print("A")

if 23 < 42:
    print("B")

###

i = 0
while i < len(line):
    print(i)
    print(line[i])
    if line[i]:
        print("C")
    print()
    i += 1

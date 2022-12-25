if True and True:
    print("A")

if True or True:
    print("B")

if [1, 2] == [3, 4]:
    print("C")

if [5, 6] == [5, 6]:
    print("D")

###

line = [True, True, False, True]
i = 0
while i < len(line) and line[i]:
    print(i)
    print(line[i])
    print()
    i += 1
print(i)
print()

###

line = [True, True, False, False, True, True]
i = 0
while i < len(line):
    if line[i]:
        j = i+1
        while j < len(line) and line[j]:
            j += 1
        print(j-i)
        i = j
    else:
        i += 1

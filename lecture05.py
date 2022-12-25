def add(a, b):
    return a+b

print(add(4, 5))

###

l = []
l.append(0)
l.append(8)
l.append(15)
print(l)

###

def nonogram(line):
    result = []
    i = 0
    while i < len(line):
        if line[i]:
            j = i+1
            while j < len(line) and line[j]:
                j += 1
            result.append(j-i)
            i = j
        else:
            i += 1
    return result

print(nonogram([True, True, False, False, True, True]))

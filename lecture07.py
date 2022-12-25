def generate_lines(length): # as before (lecture 6)
    if length == 1:
        return [[True], [False]]
    result = []
    for line in generate_lines(length-1):
        result.append([True]+line)
    for line in generate_lines(length-1):
        result.append([False]+line)
    return result

def nonogram(line): # as before (lecture 5)
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

length = 10
solution = [3, 5]

for line in generate_lines(length):
    if nonogram(line) == solution:
        print(line)

###

result = None
for line in generate_lines(length):
    if nonogram(line) == solution:
        if result is None:
            result = line
        else:
            for i in range(length):
                if result[i] != line[i]:
                    result[i] = None
print(result)

###

a = True
# a = False
# a = None

if a is None:
    print("undefined")
elif a:
    print("yes")
else:
    print("no")

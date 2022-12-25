line = ["a", "b", "c", "d", "e", "f", "g", "h"]

print(line[1], line[2], line[5], line[6])
print(line[1:], line[2:])
print(line[:5], line[:6])
print(line[1:5], line[2:6])
print(line[-2], line[-1])
print(line[:-2], line[:-1])

###

def generate_lines(old_line):
    if old_line == [None]:
        return [[True], [False]]
    if old_line == [True]:
        return [[True]]
    if old_line == [False]:
        return [[False]]
    result = []
    if old_line[0] != False:
        for line in generate_lines(old_line[1:]):
            result.append([True]+line)
    if old_line[0] != True:
        for line in generate_lines(old_line[1:]):
            result.append([False]+line)
    return result

old_line = [None, True, None]

print(generate_lines(old_line))

###

solution = [3, 3]
old_line = [None, True, None, None, None, False, None, None, None, None]

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

new_line = None
for line in generate_lines(old_line):
    if nonogram(line) == solution:
        if new_line is None:
            new_line = line
        else:
            for i in range(len(old_line)):
                if new_line[i] != line[i]:
                    new_line[i] = None
print(old_line)
print(new_line)
print(old_line != new_line)

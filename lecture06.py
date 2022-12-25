l = [True, False]
k = [False, True]

print(l+k)
print(k+l)

print([True]+l)
print([False]+l)

###

def generate_lines_len1():
    return [[True], [False]]

def generate_lines_len2():
    result = []
    for line in generate_lines_len1():
        result.append([True]+line)
    for line in generate_lines_len1():
        result.append([False]+line)
    return result

print(generate_lines_len2())

def generate_lines_len3():
    result = []
    for line in generate_lines_len2():
        result.append([True]+line)
    for line in generate_lines_len2():
        result.append([False]+line)
    return result

print(generate_lines_len3())

def generate_lines_len4():
    result = []
    for line in generate_lines_len3():
        result.append([True]+line)
    for line in generate_lines_len3():
        result.append([False]+line)
    return result

print(generate_lines_len4())

###

def generate_lines(length):
    if length == 1:
        return [[True], [False]]
    result = []
    for line in generate_lines(length-1):
        result.append([True]+line)
    for line in generate_lines(length-1):
        result.append([False]+line)
    return result

print(generate_lines(5))

print(len(generate_lines(10)))

rows = [[4],
        [1, 1],
        [1, 1],
        [4],
        [1, 2, 2],
        [1, 1, 1],
        [1, 3],
        [1, 1],
        [1, 2],
        [2]]

cols = [[8],
        [1, 1],
        [1, 1],
        [1, 1],
        [2, 1],
        [1, 1],
        [3, 2],
        [3],
        [3],
        [1]]

num_rows = len(rows)
num_cols = len(cols)

grid = [None]*num_rows*num_cols

def get_row(row):
    return grid[row*num_cols: (row+1)*num_cols]

def set_row(row, line):
    for col in range(num_cols):
        grid[row*num_cols+col] = line[col]

def get_col(col):
    return grid[col::num_cols]

def set_col(col, line):
    for row in range(num_rows):
        grid[row*num_cols+col] = line[row]

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

def improve_line(old_line, solution):
    new_line = None
    for line in generate_lines(old_line):
        if nonogram(line) == solution:
            if new_line is None:
                new_line = line
            else:
                for i in range(len(line)):
                    if new_line[i] != line[i]:
                        new_line[i] = None
    return new_line

missing = -1
while missing != 0:
    for col in range(num_cols):
        line = get_col(col)
        new_line = improve_line(line, cols[col])
        set_col(col, new_line)
    for row in range(num_rows):
        line = get_row(row)
        new_line = improve_line(line, rows[row])
        set_row(row, new_line)
    new_missing = 0
    for i in range(num_rows*num_cols):
        if grid[i] == None:
            new_missing += 1
    if new_missing == missing:
        print("Nonogram could not be solved.")
        missing = 0
    else:
        missing = new_missing

for i in range(num_rows*num_cols):
    if grid[i] is None:
        print("?", end=" ")
    elif grid[i]:
        print("*", end=" ")
    else:
        print(".", end=" ")
    if not (i+1) % num_cols:
        print()

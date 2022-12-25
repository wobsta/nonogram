import sys, collections

Nonogram = collections.namedtuple("Nonogram", "rows cols")
Grid = collections.namedtuple("Grid", "grid num_rows num_cols")

###

n = Nonogram("rows", "cols")
print(n.rows)
print(n.cols)
print()

nonogram = Nonogram([[1], [1]], [[1], [1]])
print(nonogram.rows)
print(nonogram.cols)
print()

grid = Grid([True, False, False, True], 2, 2)
print(grid.grid)
print(grid.num_rows)
print(grid.num_cols)
print()

def hello(name="world"):
    print(f"Hello, {name}!")
hello()
hello("John Doe")
print()

try:
    print("here")
    char1, char2 = "ab"
    print("there")
    char1, char2 = "abc"
    print("never")
except ValueError:
    print("There was some error, but we ignore it and continue.")

try:
    raise ValueError("Something bad happened!")
except ValueError:
    print("There was another error, but we ignore, too.")

# other stuff (open, read, readline, walrus operator, map, join ...) right in the code below

###

def get_row(grid, row):
    return grid.grid[row*grid.num_cols: (row+1)*grid.num_cols]

def set_row(grid, row, line):
    for col in range(grid.num_cols):
        grid.grid[row*grid.num_cols+col] = line[col]

def get_col(grid, col):
    return grid.grid[col::grid.num_cols]

def set_col(grid, col, line):
    for row in range(grid.num_rows):
        grid.grid[row*grid.num_cols+col] = line[row]

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

def solve(nonogram):
    grid = Grid([None]*len(nonogram.rows)*len(nonogram.cols), len(nonogram.rows), len(nonogram.cols))
    missing = -1
    while missing != 0:
        for row in range(grid.num_rows):
            line = get_row(grid, row)
            new_line = improve_line(line, nonogram.rows[row])
            set_row(grid, row, new_line)
        for col in range(grid.num_cols):
            line = get_col(grid, col)
            new_line = improve_line(line, nonogram.cols[col])
            set_col(grid, col, new_line)
        new_missing = 0
        for i in range(grid.num_rows*grid.num_cols):
            if grid.grid[i] == None:
                new_missing += 1
        if new_missing == missing:
            print("Nonogram could not be solved.")
            return grid
        missing = new_missing
    return grid

def build(grid):
    rows = []
    for row in range(grid.num_rows):
        rows.append(nonogram(get_row(grid, row)))
    cols = []
    for col in range(grid.num_cols):
        cols.append(nonogram(get_col(grid, col)))
    return Nonogram(rows, cols)

def load_nonogram(file):
    nonogram = Nonogram([], [])
    while (line := file.readline()) != "#\n":
        nonogram.rows.append(list(map(int, line.strip().split())))
    while line := file.readline():
        nonogram.cols.append(list(map(int, line.strip().split())))
    return nonogram

def dump_nonogram(nonogram, file=sys.stdout):
    for row in nonogram.rows:
        print(" ".join(map(str, row)), file=file)
    print("#", file=file)
    for col in nonogram.cols:
        print(" ".join(map(str, col)), file=file)

def load_solution(file):
    grid = []
    row = col = 0
    while item := file.read(2):
        if len(item) != 2:
            raise ValueError(f"Missing spacer at row {row+1}, column {col+1}.")
        value, spacer = item
        if value == "*":
            grid.append(True)
        elif value == ".":
            grid.append(False)
        elif value == "?":
            grid.append(None)
        else:
            raise ValueError(f"Invalid value in row {row+1}, column {col+1}.")
        if spacer == " ":
            col += 1
        elif spacer == "\n":
            if row:
                if num_cols != col+1:
                    raise ValueError(f"Different line length at row {row+1}.")
            else:
                num_cols = col+1
            col = 0
            row += 1
        else:
            raise ValueError(f"Invalid spacer in row {row+1}, column {col+1}.")
    num_rows = row
    return Grid(grid, num_rows, num_cols)

def dump_solution(grid, file=sys.stdout):
    for i in range(grid.num_rows*grid.num_cols):
        if not (i+1) % grid.num_cols:
            end = "\n"
        else:
            end = " "
        if grid.grid[i] is None:
            print("?", end=end, file=file)
        elif grid.grid[i]:
            print("*", end=end, file=file)
        else:
            print(".", end=end, file=file)

if len(sys.argv) == 1:
    g = load_solution(open("10x10.solution"))
    n = build(g)
    dump_nonogram(n)
    print()
    n = load_nonogram(open("10x10.nonogram"))
    g = solve(n)
    dump_solution(g)
else:
    # get nonograms from https://pypi.org/project/nonogram/
    n = load_nonogram(open(sys.argv[1]))
    g = solve(n)
    dump_solution(g)

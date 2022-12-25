import sys, collections

###

d = dict()
d["spam"] = "eggs"
print(d)
d = dict(spam="eggs")
print(d)
d = {"spam": "eggs"}
print(d)
print(d.keys())
print(d.values())
print(d.items())
for k in d:
    print(f"k: {d[k]}")
print()

d = collections.defaultdict(list)
print(d)
print(d["spam"])
print(d)
d["spam"].append("eggs")
print(d)
d["spam"].append("eggs")
print(d)
print()

print("ab" in "abcd")
print(8 not in [0, 8, 15])
print()

###

Nonogram = collections.namedtuple("Nonogram", "rows cols")
Grid = collections.namedtuple("Grid", "grid num_rows num_cols")

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

def generate_lines(old_line, solution):
    if old_line:
        if solution: # and (old_line[0] is None or old_line[0]):
            if all(item is None or item for item in old_line[:solution[0]]):
                if len(old_line) > solution[0] and (old_line[solution[0]] is None or not old_line[solution[0]]):
                    for l in generate_lines(old_line[solution[0]+1:], solution[1:]):
                        yield [True]*solution[0] + [False] + l
                elif len(old_line) == solution[0] and len(solution) == 1:
                    yield [True]*solution[0]
        if old_line[0] is None or not old_line[0]:
            for l in generate_lines(old_line[1:], solution):
                yield [False] + l
    elif not solution:
        yield []

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
    for line in generate_lines(old_line, solution):
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
        try:
            value, spacer = item
        except ValueError:
            raise ValueError(f"Missing spacer at row {row+1}, column {col+1}.")
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

def generate_grid(length):
    if length == 1:
        yield [True]
        yield [False]
    else:
        for grid in generate_grid(length-1):
            yield [True] + grid
            yield [False] + grid

def generate_grids(num_rows, num_cols):
    for grid in generate_grid(num_rows*num_cols):
        yield Grid(grid, num_rows, num_cols)

Solution = collections.namedtuple("Solution", "solvable grid")

solutions = collections.defaultdict(list)
for i, g in enumerate(generate_grids(4, 2)):
    n = build(g)
    solutions[str(n.rows+n.cols)].append(Solution(None not in solve(n).grid, g))

i = 0
for value in solutions.values():
    if len(value) == 1 and not value[0].solvable:
        dump_solution(value[0].grid)
        i += 1
        print()
print(i)

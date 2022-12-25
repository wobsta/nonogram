import sys, os, collections
import pgzrun

###

# WIDTH = 200
# HEIGHT = 200
#
# def draw():
#     screen.clear()
#     screen.draw.text("Hello, world!", center=(100, 100))
#     screen.draw.line((50, 150), (150, 150), "white")
#     screen.draw.filled_rect(Rect((90, 40), (20, 20)), "white")
#
# pgzrun.go()

###

TEST = "spam"

def f():
    TEST = "eggs"

def g():
    global TEST
    TEST = "eggs"

print(TEST)
f()
print(TEST)
g()
print(TEST)

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

if len(sys.argv) == 1:
    filename = "10x10.nonogram"
else:
    filename = sys.argv[1]
if open(filename).read(1) in "*.?":
    g = load_solution(open(filename))
    n = build(g)
else:
    n = load_nonogram(open(filename))
    g = Grid([None]*len(n.rows)*len(n.cols), len(n.rows), len(n.cols))

max_row_labels = max(len(row) for row in n.rows)
max_col_labels = max(len(col) for col in n.cols)

SCALE = 25
WIDTH = SCALE*(max_row_labels+len(n.cols))
HEIGHT = SCALE*(max_col_labels+len(n.rows))

def draw():
    screen.clear()
    for x, col in enumerate(n.cols):
        screen.draw.line(((x+max_row_labels)*SCALE, 0), ((x+max_row_labels)*SCALE, HEIGHT-1), "white")
        for y, label in enumerate(reversed(col)):
            screen.draw.text(str(label), center=((x+max_row_labels+0.5)*SCALE, (max_col_labels-y-0.5)*SCALE))
    for y, row in enumerate(n.rows):
        screen.draw.line((0, (y+max_col_labels)*SCALE), (WIDTH-1, (y+max_col_labels)*SCALE), "white")
        for x, label in enumerate(reversed(row)):
            screen.draw.text(str(label), center=((max_row_labels-x-0.5)*SCALE, (max_col_labels+y+0.5)*SCALE))
    if g:
        for x, col in enumerate(range(g.num_cols)):
            for y, row in enumerate(range(g.num_rows)):
                if g.grid[row*g.num_cols+col]:
                    screen.draw.filled_rect(Rect(((max_row_labels+x)*SCALE+2, (max_col_labels+y)*SCALE+2), (SCALE-3, SCALE-3)), "white")
                elif g.grid[row*g.num_cols+col] is not None:
                    screen.draw.line(((max_row_labels+x)*SCALE+4, (max_col_labels+y)*SCALE+4), ((max_row_labels+x+1)*SCALE-4, (max_col_labels+y+1)*SCALE-4), "white")
                    screen.draw.line(((max_row_labels+x+1)*SCALE-4, (max_col_labels+y)*SCALE+4), ((max_row_labels+x)*SCALE+4, (max_col_labels+y+1)*SCALE-4), "white")

def on_mouse_down(pos, button):
    col, row = pos
    col //= SCALE
    col -= max_row_labels
    row //= SCALE
    row -= max_col_labels
    if 0 <= col < g.num_cols and 0 <= row < g.num_rows:
        if button == mouse.LEFT:
            if g.grid[row*g.num_cols+col]:
                g.grid[row*g.num_cols+col] = None
            else:
                g.grid[row*g.num_cols+col] = True
        elif button == mouse.RIGHT:
            if g.grid[row*g.num_cols+col] is False:
                g.grid[row*g.num_cols+col] = None
            else:
                g.grid[row*g.num_cols+col] = False

def on_key_down(key):
    global g, n, WIDTH, HEIGHT, max_row_labels, max_col_labels
    if key == keys.B:
        n = build(g)
        max_row_labels = max(len(row) for row in n.rows)
        max_col_labels = max(len(col) for col in n.cols)
        WIDTH = SCALE*(max_row_labels+len(n.cols))
        HEIGHT = SCALE*(max_col_labels+len(n.rows))
    if key == keys.S:
        g = solve(n)

pgzrun.go()

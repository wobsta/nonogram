num_rows = 10
num_cols = 10

grid = ["a0", "b0", "c0", "d0", "e0", "f0", "g0", "h0", "i0", "j0",
        "a1", "b1", "c1", "d1", "e1", "f1", "g1", "h1", "i1", "j1",
        "a2", "b2", "c2", "d2", "e2", "f2", "g2", "h2", "i2", "j2",
        "a3", "b3", "c3", "d3", "e3", "f3", "g3", "h3", "i3", "j3",
        "a4", "b4", "c4", "d4", "e4", "f4", "g4", "h4", "i4", "j4",
        "a5", "b5", "c5", "d5", "e5", "f5", "g5", "h5", "i5", "j5",
        "a6", "b6", "c6", "d6", "e6", "f6", "g6", "h6", "i6", "j6",
        "a7", "b7", "c7", "d7", "e7", "f7", "g7", "h7", "i7", "j7",
        "a8", "b8", "c8", "d8", "e8", "f8", "g8", "h8", "i8", "j8",
        "a9", "b9", "c9", "d9", "e9", "f9", "g9", "h9", "i9", "j9"]


def grid_pos(row, col):
    return row*num_cols+col

print(grid_pos(3, 2))

def grid_val(row, col):
    return grid[row*num_cols+col]

print(grid_val(3, 2))

###

def get_row(row):
    line = []
    for col in range(num_cols):
        line.append(grid_val(row, col))
    return line

print(get_row(3))

def get_row(row):
    return grid[grid_pos(row, 0):grid_pos(row, num_cols)]

print(get_row(3))

def get_row(row):
    return grid[row*num_cols: (row+1)*num_cols]

print(get_row(3))

def get_col(col):
    line = []
    for row in range(num_rows):
        line.append(grid_val(row, col))
    return line

print(get_col(2))

def get_col(col):
    return grid[grid_pos(0, col)::num_cols]

print(get_col(2))

def get_col(col):
    return grid[col::num_cols]

print(get_col(2))

###

line = [None]*5

print(line)
print(len(line))

grid = [None]*num_rows*num_cols

print(len(grid))

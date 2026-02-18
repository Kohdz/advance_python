"""
You have a sheep of n x m grid paper and you’d like to draw a cool design on it.
You’ve decided on a block motif similar to tetris pieces.
Specifically, your picture will include the following five types of figures:


A: #

B: ###

C: ##
   ##

D: #
   ##
   #

E:  #
   ###

The array figures contains a list of letters representing the types of figures you’d like
 to include in your design. Your task is to complete a matrix of integers representing the
   grid paper and draw the figures on it according to the following rules

1. Start with a matrix of all 0’s and use a 1-based index on each figure to represent it
 on the grid. For example, if figures[0] = "E then the shape added to the grid will look like

    [
        [0, 1, 0],
        [1, 1, 1]
    ]

place the figures on the grid in the order they appear in the figures. The figures must not
overlap any other figures

2. of all the available locations, choose the one with the lowest row index

3. IIf there are multiple possible locations with the lowest row index, return a matrix
 of integers representing the grid of paper


Example:
n =4  m = 5 figures = ["D, "B, "A, , "C"]
figus = [[1, 2, 2, 2] [1, 1, 3, 0] [1,4,4,0] [0, 4, 4, 0]]
"""

n = 4
m = 5
figures = ["D", "B", "A", "C"]


# def tetris(n, m, figures):
#     geometry = {}


# output = [
#     [1, 2, 2, 2],
#     [1, 1, 3, 0],
#     [1, 4, 4, 0],
#     [0, 4, 4, 0],
# ]

# assert tetris(n, m, figures) == output


def can_place(grid, shape, row, col):
    pass    


def place_shape(grid, shape, row, col, figure_num):
    pass

def tetris(n, m, figures):
# Initialize n x m grid with 0s
    grid = [[0] * m for _ in range(n)]

    # Define the shapes as relative coordinates (row_offset, col_offset)
    # The "anchor" is always (0,0) relative to the scan loop
    shapes = {
        'A': [(0, 0)],
        'B': [(0, 0), (0, 1), (0, 2)],
        'C': [(0, 0), (0, 1), (1, 0), (1, 1)],
        'D': [(0, 0), (1, 0), (1, 1), (2, 0)],
        'E': [(0, 1), (1, 0), (1, 1), (1, 2)]
    }

    # Process each figure in the list
    for i, shape_type in enumerate(figures):
        shape_id = i + 1  # 1-based index
        shape = shapes[shape_type]
        placed = False

        # Greedy Search: Find the "lowest row index" then "lowest col index"
        # We iterate row by row, then col by col.
        for r in range(n):
            if placed: break
            for c in range(m):
                if placed: break

                # Check if the shape fits at anchor point (r, c)
                can_fit = True
                for dr, dc in shape:
                    nr, nc = r + dr, c + dc
                    
                    # Check Bounds and Overlaps
                    if not (0 <= nr < n and 0 <= nc < m and grid[nr][nc] == 0):
                        can_fit = False
                        break
                
                # If it fits, place it permanently
                if can_fit:
                    for dr, dc in shape:
                        grid[r + dr][c + dc] = shape_id
                    placed = True

    return grid

# Example 1 Data (Dimensions inferred from output)
n1, m1 = 4, 4
figures1 = ["D", "B", "A", "C"]
res1 = tetris(n1, m1, figures1)
output1 = [
    [1, 2, 2, 2],
    [1, 1, 3, 0],
    [1, 4, 4, 0],
    [0, 4, 4, 0],
]

print("Example 1 Output:")
for row in res1:
    print(row)
assert res1 == output1


print("-" * 20)

# Example 2 Data
n2, m2 = 2, 3
figures2 = ["E"]
res2 = tetris(n2, m2, figures2)
output2 = [[0, 1, 0], [1, 1, 1]]

print("Example 2 Output:")
for row in res2:
    print(row)
assert res2 == output2
from settings import COLS, NORMAL_COST, ROWS, WEIGHTED_COST

DIRECTIONS = ((-1, 0), (1, 0), (0, -1), (0, 1))


class Grid:
    def __init__(self):
        self.clear()

    def clear(self):
        self.cells = [["EMPTY"] * COLS for _ in range(ROWS)]
        self.start = (ROWS // 2, COLS // 5)
        self.goal = (ROWS // 2, COLS * 4 // 5)

    def cost(self, node):
        row, col = node
        return WEIGHTED_COST if self.cells[row][col] == "WEIGHTED" else NORMAL_COST

    def edit(self, node, state):
        if node in (self.start, self.goal):
            return False

        row, col = node
        if state == "START":
            self.start = node
            self.cells[row][col] = "EMPTY"
        elif state == "GOAL":
            self.goal = node
            self.cells[row][col] = "EMPTY"
        elif self.cells[row][col] != state:
            self.cells[row][col] = state
        else:
            return False
        return True


def get_neighbors(node, grid):
    row, col = node
    neighbors = []
    for dr, dc in DIRECTIONS:
        nr, nc = row + dr, col + dc
        if 0 <= nr < ROWS and 0 <= nc < COLS and grid.cells[nr][nc] != "WALL":
            neighbors.append((nr, nc))
    return neighbors

def build_graph(grid, weighted):
    graph = {}
    for row in range(ROWS):
        for col in range(COLS):
            if grid.cells[row][col] == "WALL":
                continue
            node = (row, col)
            neighbors = get_neighbors(node, grid)
            if weighted:
                neighbors = [(neighbor, grid.cost(neighbor)) for neighbor in neighbors]
            graph[node] = neighbors
    return graph

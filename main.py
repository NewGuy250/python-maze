import curses
from curses import wrapper
import queue
import time

# "X" is end, "O" is the starting, "#" are walls, and " " is a pathway
maze = [
    ["#", "O", "#", "#", "#", "#", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", "#", " ", "#", "#", " ", "#"],
    ["#", " ", "#", " ", " ", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "X", "#"]
]

# Visualize map
def print_maze(maze, stdscr, path=[]):
    # Color pairs
    BLUE = curses.color_pair(1)
    RED = curses.color_pair(2)
    # Print each row
    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if (i, j) in path:
                stdscr.addstr(i, j*2, "X", RED)
            else:
                stdscr.addstr(i, j*2, value, BLUE)
# Find the entrance of maze
def find_start(maze, start):
    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if value == start:
                return i, j
    return None

# Find the shortest path out
def find_path(maze, stdscr):
    start = "O"
    end = "X"
    start_pos = find_start(maze, start)
    # Initialize Queue    q = queue.Queue()
    q.put((start_pos, [start_pos]))
    # Avoid repitition
    visited = set()

    while not q.empty():
        current_pos, path = q.get()
        row, col = current_pos

        stdscr.clear()
        print_maze(maze, stdscr, path)
        # Make it so the user can see how the algorithim works
        time.sleep(0.2)
        stdscr.refresh()
        # End if X is reached
        if maze[row][col] == end:
            return path
        
        neigbors = find_neighbors(maze, row, col)

        for neighbor in neigbors:
            if neighbor in visited:
                continue

            r, c = neighbor

            if maze[r][c] == "#":
                continue
            
            new_path = path + [neighbor]
            q.put((neighbor, new_path))
            visited.add(neighbor)

# Find neighbors of a node
def find_neighbors(maze, row, col):
    neighbors = []

    if row > 0: # Up
        neighbors.append((row - 1, col))
    if row + 1 < len(maze): # Down
        neighbors.append((row + 1, col))
    if col > 0: # Left
        neighbors.append((row, col - 1))
    if col + 1 < len(maze[0]): # Right
        neighbors.append((row, col + 1))

    return neighbors

def main(stdscr):
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

    find_path(maze, stdscr)
    stdscr.getkey()

if __name__ == "__main__":
    wrapper(main)
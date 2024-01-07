import tkinter as tk
from tkinter import messagebox
import heapq

class PuzzleState:
    def __init__(self, board, parent=None, move=""):
        self.board = board
        self.parent = parent
        self.move = move
        self.cost = 0

    def __lt__(self, other):
        return self.cost < other.cost

def astar(initial_state):
    open_set = [initial_state]
    closed_set = set()

    while open_set:
        current_state = heapq.heappop(open_set)

        if is_goal_state(current_state):
            return construct_solution(current_state)

        closed_set.add(tuple(current_state.board))

        for neighbor in get_neighbors(current_state):
            if tuple(neighbor.board) not in closed_set:
                heapq.heappush(open_set, neighbor)

    return None

def is_goal_state(state):
    return state.board == [1, 2, 3, 4, 5, 6, 7, 8, 0]

def get_neighbors(state):
    neighbors = []
    empty_index = state.board.index(0)
    empty_row, empty_col = divmod(empty_index, 3)

    for move in ["up", "down", "left", "right"]:
        new_empty_row, new_empty_col = empty_row, empty_col

        if move == "up" and empty_row > 0:
            new_empty_row -= 1
        elif move == "down" and empty_row < 2:
            new_empty_row += 1
        elif move == "left" and empty_col > 0:
            new_empty_col -= 1
        elif move == "right" and empty_col < 2:
            new_empty_col += 1

        new_empty_index = 3 * new_empty_row + new_empty_col
        neighbor_board = state.board.copy()
        neighbor_board[empty_index], neighbor_board[new_empty_index] = neighbor_board[new_empty_index], neighbor_board[empty_index]

        neighbors.append(PuzzleState(neighbor_board, parent=state, move=move))

    return neighbors

def construct_solution(state):
    solution = []
    while state.parent:
        solution.insert(0, state.move)
        state = state.parent
    return solution

def move_tile(tile, buttons, solve_button):
    global animation_in_progress
    if not animation_in_progress:
        animation_in_progress = True
        index = buttons.index(tile)
        row, col = divmod(index, 3)

        empty_index = buttons.index(None)
        empty_row, empty_col = divmod(empty_index, 3)

        if (row == empty_row and abs(col - empty_col) == 1) or \
           (col == empty_col and abs(row - empty_row) == 1):
            buttons[index], buttons[empty_index] = buttons[empty_index], buttons[index]
            update_buttons(buttons)

            if is_goal_state(PuzzleState(buttons)):
                messagebox.showinfo("Puzzle 8 Solved", "Congratulations!")
                root.quit()

        update_buttons(buttons)
        root.update()
        root.after(500)
        animation_in_progress = False
        solve_button.config(state=tk.NORMAL)

def update_buttons(buttons):
    [button.grid(row=i // 3, column=i % 3) for i, button in enumerate(buttons) if button]

root = tk.Tk()
root.title("Puzzle 8")

buttons = [tk.Button(root, text=str(i + 1), width=5, height=2) for i in range(8)]
buttons.append(None)

for i, button in enumerate(buttons):
    if button:
        button.configure(command=lambda i=i: move_tile(buttons[i], buttons, solve_button))

update_buttons(buttons)

solve_button = tk.Button(root, text="Solve", command=lambda: solve_puzzle(buttons, solve_button))
solve_button.grid(row=3, column=1, columnspan=2)

animation_in_progress = False

def solve_puzzle(buttons, solve_button):
    global animation_in_progress
    if not animation_in_progress:
        animation_in_progress = True
        solve_button.config(state=tk.DISABLED)
        initial_board = [int(button["text"]) if button and button["text"] else 0 for button in buttons]
        initial_state = PuzzleState(initial_board)
        solution = astar(initial_state)

        if solution:
            apply_solution(solution, buttons, solve_button)

def apply_solution(solution, buttons, solve_button):
    global animation_in_progress
    for move in solution:
        if not animation_in_progress:
            break

        index = buttons.index(None)
        empty_row, empty_col = divmod(index, 3)

        new_empty_row = empty_row  # Initialize new_empty_row
        new_empty_col = empty_col  # Initialize new_empty_col

        if move == "up" and empty_row > 0:
            new_empty_row -= 1
        elif move == "down" and empty_row < 2:
            new_empty_row += 1
        elif move == "left" and empty_col > 0:
            new_empty_col -= 1
        elif move == "right" and empty_col < 2:
            new_empty_col += 1

        new_empty_index = 3 * new_empty_row + new_empty_col
        buttons[index], buttons[new_empty_index] = buttons[new_empty_index], buttons[index]
        update_buttons(buttons)
        root.update()
        root.after(500)

    animation_in_progress = False
    solve_button.config(state=tk.NORMAL)

if __name__ == "__main__":
    root.mainloop()
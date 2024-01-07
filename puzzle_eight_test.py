# puzzle_eight_test.py

import unittest
import tkinter as tk
from puzzle_eight import PuzzleState, astar, is_goal_state, get_neighbors, construct_solution, move_tile, update_buttons, solve_puzzle, apply_solution

class TestPuzzleSolver(unittest.TestCase):
    def test_is_goal_state(self):
        goal_state = PuzzleState([1, 2, 3, 4, 5, 6, 7, 8, 0])
        self.assertTrue(is_goal_state(goal_state))

    def test_get_neighbors(self):
        initial_state = PuzzleState([1, 2, 3, 4, 5, 6, 7, 8, 0])
        neighbors = get_neighbors(initial_state)
        self.assertEqual(len(neighbors), 4)  # Adjust based on your neighbors logic

    def test_construct_solution(self):
        state1 = PuzzleState([1, 2, 3, 4, 0, 5, 6, 7, 8])
        state2 = PuzzleState([1, 0, 3, 4, 2, 5, 6, 7, 8])
        state3 = PuzzleState([1, 2, 3, 4, 5, 6, 7, 8, 0])

        state2.parent = state1
        state3.parent = state2

        solution = construct_solution(state3)
        self.assertEqual(solution, ["up", "left"])

    def test_move_tile(self):
        root = tk.Tk()
        buttons = [tk.Button(root, text=str(i + 1), width=5, height=2, command=lambda button=button: move_tile(button, buttons)) for i, button in enumerate([None] * 8)]
        buttons[7] = tk.Button(root, text="", width=5, height=2)  # Empty button

        # Manually set the button text for testing
        buttons[1]["text"] = "2"
        buttons[5]["text"] = "6"

        move_tile(buttons[1], buttons)
        self.assertEqual(buttons[1]["text"], "")
        self.assertEqual(buttons[7]["text"], "2")

        move_tile(buttons[5], buttons)
        self.assertNotEqual(buttons[5]["text"], "")
        self.assertEqual(buttons[7]["text"], "6")

        root.destroy()

if __name__ == '__main__':
    unittest.main()
import tkinter as tk
from tkinter import messagebox
import numpy as np
import random

class SudokuGUI:
    def __init__(self, master):
        self.master = master
        master.title("Sudoku Generator & Solver")

        self.entries = [[None for _ in range(9)] for _ in range(9)]
        self.grid = np.zeros((9, 9), dtype=int)

        self.create_grid()
        self.create_buttons()

    def create_grid(self):
        for i in range(9):
            for j in range(9):
                e = tk.Entry(self.master, width=2, font=('Arial', 18), justify='center')
                e.grid(row=i, column=j, padx=1, pady=1, ipadx=5, ipady=5)
                self.entries[i][j] = e

    def create_buttons(self):
        generate_button = tk.Button(self.master, text="Generate", command=self.generate)
        generate_button.grid(row=9, column=0, columnspan=3)

        solve_button = tk.Button(self.master, text="Solve", command=self.solve)
        solve_button.grid(row=9, column=3, columnspan=3)

        clear_button = tk.Button(self.master, text="Clear", command=self.clear)
        clear_button.grid(row=9, column=6, columnspan=3)

    def generate(self):
        self.grid = self.generate_sudoku()
        self.update_grid(self.grid)

    def update_grid(self, grid):
        for i in range(9):
            for j in range(9):
                val = grid[i][j]
                self.entries[i][j].delete(0, tk.END)
                if val != 0:
                    self.entries[i][j].insert(0, str(val))

    def read_grid(self):
        for i in range(9):
            for j in range(9):
                val = self.entries[i][j].get()
                self.grid[i][j] = int(val) if val.isdigit() else 0

    def clear(self):
        for i in range(9):
            for j in range(9):
                self.entries[i][j].delete(0, tk.END)

    def solve(self):
        self.read_grid()
        if self.solve_sudoku(self.grid):
            self.update_grid(self.grid)
        else:
            messagebox.showerror("Error", "No solution exists!")

    # Sudoku Solver (Backtracking)
    def is_valid(self, grid, row, col, num):
        block_row, block_col = row // 3 * 3, col // 3 * 3
        return (num not in grid[row] and
                num not in grid[:, col] and
                num not in grid[block_row:block_row + 3, block_col:block_col + 3])

    def solve_sudoku(self, grid):
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    for num in range(1, 10):
                        if self.is_valid(grid, i, j, num):
                            grid[i][j] = num
                            if self.solve_sudoku(grid):
                                return True
                            grid[i][j] = 0
                    return False
        return True

    # Sudoku Generator (simple version)
    def generate_sudoku(self):
        base_grid = np.zeros((9, 9), dtype=int)
        self.fill_diagonal_boxes(base_grid)
        self.solve_sudoku(base_grid)
        return self.remove_elements(base_grid, 40)

    def fill_diagonal_boxes(self, grid):
        for i in range(0, 9, 3):
            self.fill_box(grid, i, i)

    def fill_box(self, grid, row, col):
        nums = list(range(1, 10))
        random.shuffle(nums)
        for i in range(3):
            for j in range(3):
                grid[row + i][col + j] = nums.pop()

    def remove_elements(self, grid, count):
        puzzle = grid.copy()
        attempts = 0
        while count > 0 and attempts < 100:
            row, col = random.randint(0, 8), random.randint(0, 8)
            if puzzle[row][col] != 0:
                puzzle[row][col] = 0
                count -= 1
            attempts += 1
        return puzzle

if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()
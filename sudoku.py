import tkinter as tk
from tkinter import messagebox
import random
import copy

# Sudoku logic
def generate_full_board():
    board = [[0 for _ in range(9)] for _ in range(9)]
    fill_board(board)
    return board

def fill_board(board):
    empty = find_empty(board)
    if not empty:
        return True
    row, col = empty
    nums = list(range(1, 10))
    random.shuffle(nums)
    for num in nums:
        if is_valid(board, num, (row, col)):
            board[row][col] = num
            if fill_board(board):
                return True
            board[row][col] = 0
    return False

def generate_puzzle(board, difficulty=40):
    puzzle = copy.deepcopy(board)
    attempts = difficulty
    while attempts > 0:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        if puzzle[row][col] != 0:
            puzzle[row][col] = 0
            attempts -= 1
    return puzzle

def is_valid(board, num, pos):
    row, col = pos
    if num in board[row]:
        return False
    if num in [board[i][col] for i in range(9)]:
        return False
    box_x = col // 3
    box_y = row // 3
    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if board[i][j] == num:
                return False
    return True

def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return i, j
    return None

def is_solved(board):
    return find_empty(board) is None

# GUI
class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku")
        self.entries = [[None for _ in range(9)] for _ in range(9)]
        self.full_board = generate_full_board()
        self.puzzle = generate_puzzle(self.full_board)
        self.user_board = copy.deepcopy(self.puzzle)

        # Updated colors: first region is light blue, rest are soft pastels
        self.colors = [
            "#b3e5fd", "#e6f7ff", "#fff0f5",
            "#e6ffe6", "#ffffcc", "#f9e6ff",
            "#ffe6cc", "#ccffff", "#e6e6fa"
        ]

        self.build_gui()

    def build_gui(self):
        frame = tk.Frame(self.root, padx=5, pady=5)
        frame.pack()

        for i in range(9):
            for j in range(9):
                color = self.get_region_color(i, j)
                entry = tk.Entry(
                    frame,
                    width=2,
                    font=('Arial', 18),
                    justify='center',
                    bg=color,
                    bd=1,
                    relief='solid',
                    disabledbackground=color,  # pre-filled color match
                    disabledforeground='black'  # default black can be changed if you want color matching
                )
                entry.grid(row=i, column=j, padx=1, pady=1)

                if self.puzzle[i][j] != 0:
                    entry.insert(0, str(self.puzzle[i][j]))
                    entry.config(state='disabled')
                else:
                    entry.bind("<FocusOut>", lambda e, row=i, col=j: self.check_input(row, col))

                self.entries[i][j] = entry

        self.status = tk.Label(self.root, text="Fill in the board!", font=('Arial', 14))
        self.status.pack(pady=10)

        btn = tk.Button(self.root, text="Restart", command=self.restart)
        btn.pack(pady=5)

    def get_region_color(self, row, col):
        region = (row // 3) * 3 + (col // 3)
        return self.colors[region]

    def check_input(self, row, col):
        entry = self.entries[row][col]
        val = entry.get()

        if val.isdigit() and 1 <= int(val) <= 9:
            num = int(val)
            if is_valid(self.user_board, num, (row, col)):
                self.user_board[row][col] = num
                if is_solved(self.user_board):
                    self.status.config(text="You solved it! 🎉")
                    messagebox.showinfo("Sudoku", "Congratulations, you won!")
            else:
                entry.delete(0, tk.END)
                self.status.config(text="Invalid move.")
        else:
            entry.delete(0, tk.END)
            self.status.config(text="Enter numbers 1–9.")

    def restart(self):
        self.full_board = generate_full_board()
        self.puzzle = generate_puzzle(self.full_board)
        self.user_board = copy.deepcopy(self.puzzle)

        for i in range(9):
            for j in range(9):
                entry = self.entries[i][j]
                color = self.get_region_color(i, j)
                entry.config(state='normal', bg=color, disabledbackground=color)
                entry.delete(0, tk.END)
                if self.puzzle[i][j] != 0:
                    entry.insert(0, str(self.puzzle[i][j]))
                    entry.config(state='disabled')

        self.status.config(text="New game started!")

# Run the game
if __name__ == "__main__":
    root = tk.Tk()
    SudokuGUI(root)
    root.mainloop()

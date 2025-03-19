import tkinter as tk
from tkinter import messagebox
import random

class Minesweeper:
    def __init__(self, root, rows=15, cols=15, mines=20):
        self.root = root
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.board = [[0 for _ in range(cols)] for _ in range(rows)]
        self.buttons = [[None for _ in range(cols)] for _ in range(rows)]
        self.game_over = False

        self.create_widgets()
        self.place_mines()
        self.calculate_adjacent_mines()

    def create_widgets(self):
        for r in range(self.rows):
            for c in range(self.cols):
                btn = tk.Button(self.root, width=3, height=1, 
                                command=lambda r=r, c=c: self.reveal_cell(r, c))
                btn.bind("<Button-3>", lambda event, r=r, c=c: self.flag_cell(r, c))
                btn.grid(row=r, column=c)
                self.buttons[r][c] = btn

    def place_mines(self):
        count = 0
        while count < self.mines:
            r, c = random.randint(0, self.rows - 1), random.randint(0, self.cols - 1)
            if self.board[r][c] != -1:
                self.board[r][c] = -1
                count += 1

    def calculate_adjacent_mines(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] == -1:
                    continue
                count = sum(self.board[rr][cc] == -1 for rr in range(r-1, r+2) 
                            for cc in range(c-1, c+2) if 0 <= rr < self.rows and 0 <= cc < self.cols)
                self.board[r][c] = count

    def reveal_cell(self, r, c):
        if self.game_over or self.buttons[r][c]["state"] == "disabled":
            return

        if self.board[r][c] == -1:
            self.buttons[r][c].config(text="💣", bg="red")
            self.end_game(False)
        else:
            self.buttons[r][c].config(text=str(self.board[r][c]) if self.board[r][c] > 0 else "", state="disabled", relief=tk.SUNKEN)
            if self.board[r][c] == 0:
                for rr in range(r-1, r+2):
                    for cc in range(c-1, c+2):
                        if 0 <= rr < self.rows and 0 <= cc < self.cols:
                            self.reveal_cell(rr, cc)
        self.check_win()

    def flag_cell(self, r, c):
        if self.game_over or self.buttons[r][c]["state"] == "disabled":
            return
        current_text = self.buttons[r][c]["text"]
        self.buttons[r][c].config(text="🚩" if current_text == "" else "")

    def check_win(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] != -1 and self.buttons[r][c]["state"] != "disabled":
                    return
        self.end_game(True)

    def end_game(self, won):
        self.game_over = True
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] == -1:
                    self.buttons[r][c].config(text="💣", bg="green" if won else "red")
        message = "You Win!" if won else "Game Over!"
        self.root.after(500, lambda: messagebox.showinfo("Game Over", message))

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Minesweeper")
    game = Minesweeper(root)
    root.mainloop()

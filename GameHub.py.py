import tkinter as tk
from tkinter import messagebox
import random

class GameHub:
    def __init__(self, master):
        self.master = master
        self.master.title("Game Hub")
        self.center_window(400,300)
        self.create_interface()

    def center_window(self, width, height):
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.master.geometry(f"{width}x{height}+{x}+{y}")


    def create_interface(self):
        tk.Label(self.master, text="Welcome to Game Hub!", font=('consolas', 24)).pack(pady=20)

        tk.Button(self.master, text="Play Tic-Tac-Toe", font=('consolas', 18), command=self.launch_tictactoe).pack(pady=10)
        tk.Button(self.master, text="Play Snake", font=('consolas', 18), command=self.launch_snake).pack(pady=10)
        tk.Button(self.master, text="Play Connect Four", font=('consolas', 18), command=self.launch_connectfour).pack(pady=10)

    def launch_tictactoe(self):
        self.master.withdraw()
        TicTacToe(self.master)

    def launch_snake(self):
        self.master.withdraw()
        SnakeGame(self.master)

    def launch_connectfour(self):
        self.master.withdraw()
        ConnectFour(self.master)

    def return_to_hub(self):
        self.master.deiconify()

# Tic-Tac-Toe Game Implementation
class TicTacToe:
    def __init__(self, master):
        self.master=master
        self.tictactoe_window = tk.Toplevel(master)
        self.tictactoe_window.title("Tic-Tac-Toe")
        self.board = ["-", "-", "-", "-", "-", "-", "-", "-", "-"]
        self.currentPlayer = "X"
        self.winner = None
        self.gameRunning = True
        self.create_board()

    def create_board(self):
        self.buttons = []
        for i in range(9):
            button = tk.Button(self.tictactoe_window, text="", font=('consolas', 20), width=5, height=2,
                               command=lambda i=i: self.player_move(i))
            button.grid(row=i // 3, column=i % 3)
            self.buttons.append(button)

    def player_move(self, index):
        if self.board[index] == "-" and self.gameRunning:
            self.board[index] = self.currentPlayer
            self.buttons[index].config(text=self.currentPlayer)
            self.check_winner()
            if not self.winner:
                self.currentPlayer = "O" if self.currentPlayer == "X" else "X"
                self.computer_move()

    def computer_move(self):
        available_moves = [i for i, spot in enumerate(self.board) if spot == "-"]
        if available_moves:
            move = random.choice(available_moves)
            self.board[move] = self.currentPlayer
            self.buttons[move].config(text=self.currentPlayer)
            self.check_winner()
            self.currentPlayer = "O" if self.currentPlayer == "X" else "X"

    def check_winner(self):
        for combo in [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] and self.board[combo[0]] != "-":
                self.winner = self.board[combo[0]]
                self.gameRunning = False
                messagebox.showinfo("Tic-Tac-Toe", f"{self.winner} wins!")
                self.return_to_hub()

        if "-" not in self.board and not self.winner:
            messagebox.showinfo("Tic-Tac-Toe", "It's a tie!")
            self.gameRunning = False
            self.return_to_hub()

    def return_to_hub(self):
        self.tictactoe_window.destroy()
        self.master.deiconify()

# Snake Game Implementation
class SnakeGame:
    def __init__(self, master):
        self.master=master
        self.snake_window = tk.Toplevel(master)
        self.snake_window.title("Snake")
        self.rows = 20
        self.columns = 20
        self.speed = 100
        self.snake_direction = "down"
        self.snake_parts = [[0, 0], [0, 1], [0, 2]]
        self.food = None
        self.create_board()

    def create_board(self):
        self.canvas = tk.Canvas(self.snake_window, width=400, height=400, bg="black")
        self.canvas.pack()

        self.snake = [self.canvas.create_rectangle(x * 20, y * 20, x * 20 + 20, y * 20 + 20, fill="green") for x, y in self.snake_parts]

        self.place_food()

        self.snake_window.bind("<Up>", lambda e: self.change_direction("up"))
        self.snake_window.bind("<Down>", lambda e: self.change_direction("down"))
        self.snake_window.bind("<Left>", lambda e: self.change_direction("left"))
        self.snake_window.bind("<Right>", lambda e: self.change_direction("right"))

        self.move_snake()

    def place_food(self):
        self.canvas.delete("food")
        while True:
            x = random.randint(0, self.columns - 1)
            y = random.randint(0, self.rows - 1)
            if [x, y] not in self.snake_parts:
                self.food = [x, y]
                break
        self.canvas.create_rectangle(x * 20, y * 20, x * 20 + 20, y * 20 + 20, fill="red", tag="food")

    def change_direction(self, new_direction):
        opposite_directions = [("up", "down"), ("left", "right")]
        if (self.snake_direction, new_direction) not in opposite_directions:
            self.snake_direction = new_direction

    def move_snake(self):
        head_x, head_y = self.snake_parts[-1]
        if self.snake_direction == "up":
            head_y -= 1
        elif self.snake_direction == "down":
            head_y += 1
        elif self.snake_direction == "left":
            head_x -= 1
        elif self.snake_direction == "right":
            head_x += 1

        head_x %= self.columns
        head_y %= self.rows

        if head_x < 0 or head_x >= self.columns or head_y < 0 or head_y >= self.rows or [head_x, head_y] in self.snake_parts:
            messagebox.showinfo("Snake", "Game Over!")
            self.return_to_hub()
            return

        self.snake_parts.append([head_x, head_y])
        self.snake.append(self.canvas.create_rectangle(head_x * 20, head_y * 20, head_x * 20 + 20, head_y * 20 + 20, fill="green"))

        if [head_x, head_y] == self.food:
            self.place_food()
        else:
            del self.snake_parts[0]
            self.canvas.delete(self.snake.pop(0))

        self.snake_window.after(self.speed, self.move_snake)

    def return_to_hub(self):
        self.snake_window.destroy()
        self.master.deiconify()

# Connect Four Game Implementation
class ConnectFour:
    def __init__(self, master):
        self.master=master
        self.connect4_window = tk.Toplevel(master)
        self.connect4_window.title("Connect Four")
        self.rows = 6
        self.columns = 7
        self.player = "Red"
        self.board = [["" for _ in range(self.columns)] for _ in range(self.rows)]
        self.create_board()

    def create_board(self):
        self.buttons = []
        for col in range(self.columns):
            button = tk.Button(self.connect4_window, text=f"Col {col+1}", command=lambda c=col: self.user_move(c))
            button.grid(row=0, column=col)
            self.buttons.append(button)

        self.cells = []
        for row in range(1, self.rows + 1):
            row_cells = []
            for col in range(self.columns):
                cell = tk.Canvas(self.connect4_window, width=80, height=80, bg="blue", highlightthickness=0)
                cell.grid(row=row, column=col)
                row_cells.append(cell)
            self.cells.append(row_cells)

    def user_move(self, col):
        if self.drop_disc(col, "Red"):
            if self.check_winner("Red"):
                messagebox.showinfo("Connect Four", "Player Red wins!")
                self.return_to_hub()
            else:
                self.connect4_window.after(500, self.computer_move)

    def computer_move(self):
        available_columns = [col for col in range(self.columns) if self.board[0][col] == ""]
        if available_columns:
            col = random.choice(available_columns)
            self.drop_disc(col, "Black")
            if self.check_winner("Black"):
                messagebox.showinfo("Connect Four", "Player Black wins!")
                self.return_to_hub()

    def drop_disc(self, col, player):
        for row in range(self.rows - 1, -1, -1):
            if self.board[row][col] == "":
                self.board[row][col] = player
                self.cells[row][col].create_oval(10, 10, 70, 70, fill=player)
                return True
        return False

    def check_winner(self, player):
        for row in range(self.rows):
            for col in range(self.columns):
                if (self.check_direction(row, col, player, 1, 0) or  # Horizontal
                    self.check_direction(row, col, player, 0, 1) or  # Vertical
                    self.check_direction(row, col, player, 1, 1) or  # Diagonal /
                    self.check_direction(row, col, player, 1, -1)):  # Diagonal \
                    return True
        return False

    def check_direction(self, row, col, player, row_step, col_step):
        count = 0
        for step in range(4):
            r = row + step * row_step
            c = col + step * col_step
            if 0 <= r < self.rows and 0 <= c < self.columns and self.board[r][c] == player:
                count += 1
            else:
                break
        return count == 4

    def return_to_hub(self):
        self.connect4_window.destroy()
        self.master.deiconify()

# Main Execution
if __name__ == "__main__":
    root = tk.Tk()
    app = GameHub(root)
    root.mainloop()

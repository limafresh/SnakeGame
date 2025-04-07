import tkinter as tk
from tkinter import colorchooser, messagebox
import random


class SnakeGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.resizable(False, False)

        self.width = 300
        self.height = 200
        self.snake_color = "chartreuse"
        self.food_color = "orange red"
        self.bg_color = "black"
        self.speed = 200
        self.level = 1
        self.game_over = True
        self.is_pause = True

        self.menu_bar = tk.Menu(self)

        self.menu_bar.add_command(label="Restart", command=self.new_game)

        self.settings_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Settings", menu=self.settings_menu)
        level_menu = tk.Menu(self.settings_menu, tearoff=0)
        self.settings_menu.add_cascade(label="Level", menu=level_menu)
        levels = ["1", "2", "3", "4", "5", "6", "7", "8"]
        for level in levels:
            level_menu.add_command(
                label=level, command=lambda level=level: self.change_level(level)
            )
        self.settings_menu.add_command(
            label="Snake color", command=self.change_snake_color
        )
        self.settings_menu.add_command(
            label="Food color", command=self.change_food_color
        )
        self.settings_menu.add_command(
            label="Background color", command=self.change_bg_color
        )

        self.menu_bar.add_command(label="About", command=self.about)
        self.menu_bar.add_command(label="Pause", command=self.pause)

        self.config(menu=self.menu_bar)

        self.canvas = tk.Canvas(
            self, width=self.width, height=self.height, bg=self.bg_color
        )
        self.canvas.pack()

        self.new_game()

        self.bind("<KeyPress>", self.change_direction)
        self.bind("<Control-p>", self.pause)
        self.bind("<Control-n>", self.new_game)

    def game_loop(self):
        if self.game_over:
            self.menu_bar.entryconfig(1, state=tk.NORMAL)
            self.settings_menu.entryconfig("Level", state=tk.NORMAL)
            self.menu_bar.entryconfig(4, state=tk.DISABLED)
            messagebox.showinfo("Game over", f"Game over. Score: {self.score}")
            return
        if self.is_pause:
            return

        self.move_snake()
        self.check_collisions()
        self.update_snake()

        self.after(self.speed, self.game_loop)

    def update_snake(self):
        self.canvas.delete("snake")
        for segment in self.snake:
            self.canvas.create_rectangle(
                segment[0],
                segment[1],
                segment[0] + 10,
                segment[1] + 10,
                fill=self.snake_color,
                outline=self.bg_color,
                tags="snake",
            )

    def move_snake(self):
        head_x, head_y = self.snake[0]
        if self.snake_direction == "Right":
            head_x += 10
        elif self.snake_direction == "Left":
            head_x -= 10
        elif self.snake_direction == "Up":
            head_y -= 10
        elif self.snake_direction == "Down":
            head_y += 10

        new_head = (head_x, head_y)
        self.snake = [new_head] + self.snake[:-1]

        if new_head == self.food:
            self.canvas.delete("food")
            self.snake.append(self.snake[-1])
            self.score = self.score + 1 * self.level
            self.title(f"Score: {self.score}")
            self.create_food()

    def create_food(self):
        food_x, food_y = self.generate_food_position()
        self.food = (food_x, food_y)
        self.canvas.create_rectangle(
            food_x,
            food_y,
            food_x + 10,
            food_y + 10,
            fill=self.food_color,
            outline=self.bg_color,
            tags="food",
        )

    def generate_food_position(self):
        while True:
            food_x = random.randint(0, (self.width - 10) // 10) * 10
            food_y = random.randint(0, (self.height - 10) // 10) * 10
            if (food_x, food_y) not in self.snake:
                return food_x, food_y

    def change_direction(self, event):
        if event.keysym == "Left" and self.snake_direction != "Right":
            self.snake_direction = "Left"
        elif event.keysym == "Right" and self.snake_direction != "Left":
            self.snake_direction = "Right"
        elif event.keysym == "Up" and self.snake_direction != "Down":
            self.snake_direction = "Up"
        elif event.keysym == "Down" and self.snake_direction != "Up":
            self.snake_direction = "Down"

    def check_collisions(self):
        head_x, head_y = self.snake[0]
        if head_x < 0 or head_x >= self.width or head_y < 0 or head_y >= self.height:
            self.game_over = True
        if (head_x, head_y) in self.snake[1:]:
            self.game_over = True

    def new_game(self, event=None):
        if not self.game_over:
            return
        self.canvas.delete("all")
        self.menu_bar.entryconfig(1, state=tk.DISABLED)
        self.settings_menu.entryconfig("Level", state=tk.DISABLED)
        self.menu_bar.entryconfig(4, state=tk.NORMAL)

        self.snake = [(100, 100), (90, 100), (80, 100)]
        self.snake_direction = "Right"
        self.food = None
        self.score = 0
        self.title(f"Score: {self.score}")
        self.create_food()

        self.game_over = False
        self.is_pause = False
        self.update_snake()
        self.after(self.speed, self.game_loop)

    def change_snake_color(self):
        color_code = colorchooser.askcolor(title="Choose snake color")[1]
        if color_code:
            self.snake_color = color_code
            self.canvas.itemconfig("snake", fill=self.snake_color)

    def change_food_color(self):
        color_code = colorchooser.askcolor(title="Choose food color")[1]
        if color_code:
            self.food_color = color_code
            self.canvas.itemconfig("food", fill=self.food_color)

    def change_bg_color(self):
        color_code = colorchooser.askcolor(title="Choose background color")[1]
        if color_code:
            self.bg_color = color_code
            self.canvas["bg"] = self.bg_color
            self.canvas.itemconfig("snake", outline=self.bg_color)
            self.canvas.itemconfig("food", outline=self.bg_color)

    def change_level(self, level):
        self.level = int(level)
        var = 9 - int(level)
        self.speed = int(25 * var)

    def about(self):
        message_text = """Control the snake with the arrow keys and collect food.
The higher the level, the faster the snake moves and the more points.

Hotkeys: Ctrl+N - new game, Ctrl+P - pause/continue.

Author: limafresh <https://github.com/limafresh>"""
        messagebox.showinfo("About Snake game", message_text)

    def pause(self, event=None):
        if self.game_over:
            return
        if not self.is_pause:
            self.is_pause = True
            self.menu_bar.entryconfig(4, label="Continue")
        elif self.is_pause:
            self.is_pause = False
            self.after(self.speed, self.game_loop)
            self.menu_bar.entryconfig(4, label="Pause")


SnakeGame().mainloop()

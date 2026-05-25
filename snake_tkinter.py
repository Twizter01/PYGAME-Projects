import tkinter
import random

# Constants
ROWS, COLS = 25, 25
TILE_SIZE = 25
WINDOW_WIDTH, WINDOW_HEIGHT = COLS * TILE_SIZE, ROWS * TILE_SIZE

class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Game Window
window = tkinter.Tk()
window.title("Snake")
window.resizable(False, False)

# Canvas
canvas = tkinter.Canvas(window, bg='black', width=WINDOW_WIDTH, height=WINDOW_HEIGHT, borderwidth=0, highlightthickness=0)
canvas.pack()
window.update()

# Center Window
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_x = int((screen_width/2) - (window_width/2))
window_y = int((screen_height/2) - (window_width/2))

window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")


# Window Mainloop
snake = Tile(5*TILE_SIZE, 5*TILE_SIZE)
food = Tile(10*TILE_SIZE, 10*TILE_SIZE)
velocity_x = 0
velocity_y = 0
snake_body = [] # Multuiple Snake Tiles
game_over = False
score = 0

def change_direction(event):
    global velocity_x, velocity_y
    if game_over:
        return
    
    if (event.keysym == "w" and velocity_y != 1):
        velocity_x = 0
        velocity_y = -1
    elif (event.keysym == "s" and velocity_y != -1):  # Fixed: velocity_y (not velocity_x)
        velocity_x = 0
        velocity_y = 1
    elif (event.keysym == "a" and velocity_x != 1):
        velocity_x = -1
        velocity_y = 0
    elif (event.keysym == "d" and velocity_x != -1):  # Fixed: velocity_x (not velocity_y)
        velocity_x = 1
        velocity_y = 0

def move():
    global snake, food, snake_body, game_over, score

    if game_over:
        return
    if snake.x < 0 or snake.x >= WINDOW_WIDTH or snake.y < 0 or snake.y >= WINDOW_HEIGHT:
        game_over = True
        return
    for tile in snake_body:
        if snake.x == tile.x and snake.y == tile.y:
            game_over = True
            return


    # Collission Detection
    if snake.x == food.x and snake.y == food.y:
        snake_body.append(Tile(food.x, food.y))
        food.x = random.randint(0, COLS - 1) * TILE_SIZE
        food.y = random.randint(0, ROWS - 1) * TILE_SIZE
        score += 1
    

    # Update Snake Body
    for i in range(len(snake_body) - 1, -1, -1): # Check the body of the snake backwards
        tile = snake_body[i]
        if i == 0:
            tile.x = snake.x
            tile.y = snake.y
        else:
            prev_tile = snake_body[i-1]
            tile.x = prev_tile.x
            tile.y = prev_tile.y

    snake.x += velocity_x * TILE_SIZE
    snake.y += velocity_y * TILE_SIZE
    

def draw():
    global snake, running

    move()
    canvas.delete('all')

    # Draw Food
    canvas.create_rectangle(food.x, food.y, food.x + TILE_SIZE, food.y + TILE_SIZE, fill='purple')

    # Draw Snake
    canvas.create_rectangle(snake.x, snake.y, snake.x + TILE_SIZE, snake.y + TILE_SIZE, fill='lime green')
    for tile in snake_body:
        canvas.create_rectangle(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill='lime green')

    if game_over:
        #canvas.create_text(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, font= "Arial 15", text=f"Total Score{score}", fill='white')
        canvas.create_text(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, font= 'Arial 40', text="Game Over", fill='white') 
        canvas.create_text(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50, font= 'Arial 20', text="Play Again? Press Spacebar", fill='white')
        
        if window.bind("<KeyRelease>") == "space":
            running = not running
        else:
            running = False

   
    else:
        canvas.create_text(40, 15, font= "Arial 15", text=f"Score: {score}", fill='purple')

    
    # Update Screen every 100ms and call draw again
    window.after(100, draw)

running = True
while running:
    draw()

    window.bind("<KeyRelease>", change_direction)
    window.mainloop()
    
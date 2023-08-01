import pygame
import random

pygame.init()

# Constants
WIDTH, HEIGHT = 400, 400
ROWS, COLS = 4, 4
TILE_SIZE = WIDTH // COLS
BORDER_SIZE = 5
GRID_SIZE = TILE_SIZE * ROWS + BORDER_SIZE * (ROWS - 1)
BACKGROUND_COLOR = (187, 173, 160)
BORDER_COLOR = (185, 122, 87)
TILE_COLORS = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
}
FONT_SIZE = 40
FONT_COLOR = (119, 110, 101)

# Initialize the window :)
win = pygame.display.set_mode((GRID_SIZE, GRID_SIZE))
pygame.display.set_caption('2048')

# Function to draw the grid and tiles
def draw_grid():
    win.fill(BORDER_COLOR)
    for row in range(ROWS):
        for col in range(COLS):
            tile_value = grid[row][col]
            color = TILE_COLORS[tile_value]
            tile_x, tile_y = col * (TILE_SIZE + BORDER_SIZE), row * (TILE_SIZE + BORDER_SIZE)

            # Draw border around each tile
            tile_rect = pygame.Rect(tile_x, tile_y, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(win, BORDER_COLOR, tile_rect)

            # Draw tile
            tile_inner_rect = pygame.Rect(tile_x + BORDER_SIZE, tile_y + BORDER_SIZE, TILE_SIZE - BORDER_SIZE, TILE_SIZE - BORDER_SIZE)
            pygame.draw.rect(win, color, tile_inner_rect)

            if tile_value != 0:
                font = pygame.font.SysFont('Arial', FONT_SIZE)
                text = font.render(str(tile_value), True, FONT_COLOR)
                text_rect = text.get_rect(center=(tile_x + TILE_SIZE // 2, tile_y + TILE_SIZE // 2))
                win.blit(text, text_rect)

    # Draw border around the entire grid
    pygame.draw.rect(win, BORDER_COLOR, (0, 0, GRID_SIZE, GRID_SIZE), BORDER_SIZE)

# Function to add a new tile (2 or 4) to the grid
def add_new_tile():
    empty_cells = [(row, col) for row in range(ROWS) for col in range(COLS) if grid[row][col] == 0]
    if empty_cells:
        row, col = random.choice(empty_cells)
        grid[row][col] = random.choice([2, 4])

# Function to slide and merge tiles to the left in a given row
def slide_and_merge(row):
    new_row = [tile for tile in row if tile != 0]
    for i in range(len(new_row) - 1):
        if new_row[i] == new_row[i + 1]:
            new_row[i] *= 2
            new_row[i + 1] = 0
    new_row = [tile for tile in new_row if tile != 0]
    return new_row + [0] * (len(row) - len(new_row))

# Function to handle left movement
def move_left():
    global grid
    for row in range(ROWS):
        new_row = slide_and_merge(grid[row])
        grid[row] = new_row + [0] * (COLS - len(new_row))
    add_new_tile()

# Function to handle right movement
def move_right():
    global grid
    for row in range(ROWS):
        new_row = slide_and_merge(grid[row][::-1])
        grid[row] = [0] * (COLS - len(new_row)) + new_row[::-1]
    add_new_tile()

# Function to handle up movement
def move_up():
    global grid
    for col in range(COLS):
        col_values = [grid[row][col] for row in range(ROWS)]
        new_col = slide_and_merge(col_values)
        for row in range(ROWS):
            grid[row][col] = new_col[row] if row < len(new_col) else 0
    add_new_tile()

# Function to handle down movement
def move_down():
    global grid
    for col in range(COLS):
        col_values = [grid[row][col] for row in range(ROWS)][::-1]
        new_col = slide_and_merge(col_values)
        for row in range(ROWS):
            grid[row][col] = new_col[ROWS - row - 1] if row < len(new_col) else 0
    add_new_tile()

# Initialize the game grid
grid = [[0] * COLS for _ in range(ROWS)]

# Add two initial tiles to the grid
add_new_tile()
add_new_tile()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move_left()
            elif event.key == pygame.K_RIGHT:
                move_right()
            elif event.key == pygame.K_UP:
                move_up()
            elif event.key == pygame.K_DOWN:
                move_down()

    draw_grid()
    pygame.display.flip()

pygame.quit()

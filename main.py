import pygame
import time
import os

# ─────────────────────────────────────────
#  PYGAME CONFIG
# ─────────────────────────────────────────
pygame.init()
start_time = time.time()
BASE_DIR     = os.path.dirname(os.path.abspath(__file__))
WINDOW_WIDTH, WINDOW_HEIGHT = 1680, 820
WINDOW       = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Lateral Movement Test')
CLOCK        = pygame.time.Clock()
FPS          = 60

current_time = time.time() - start_time

# ───────────────────────────────────────── -> This can change depending on your sprite dimensions so calculate accordingly
#  SPRITE SHEET DIMENSIONS
#  Sheet: 192x384 → 8 cols x 8 rows
#  Each frame: 24x48px, displayed at 3x → 72x144px
# ─────────────────────────────────────────
FRAME_WIDTH   = 88
FRAME_HEIGHT  = 88
FRAME_COUNT   = 4 # columnas = frames por animacion
DISPLAY_SCALE = 3 # escalar 3x para que se vea bien

DISPLAY_W = FRAME_WIDTH  * DISPLAY_SCALE  # 72pxa
DISPLAY_H = FRAME_HEIGHT * DISPLAY_SCALE  # 144px

# ─────────────────────────────────────────
#  DIRECTION ROWS
#  Cada fila del sheet = una direccion
# ─────────────────────────────────────────
DIRECTION_ROWS = {
    'down':         0,
    'down-right':   1,
    'right':        2,
    'up-right':     3,
    'up':           4,
    'up-left':      5,
    'left':         6,
    'down-left':    7
}

# ─────────────────────────────────────────
#  PHYSICS
# ─────────────────────────────────────────
GRAVITY    =  0.4   # aceleracion hacia abajo cada frame
FLAP_FORCE = -11    # impulso hacia arriba al presionar espacio

# ─────────────────────────────────────────
#  get_frames()
#  Corta una fila del sprite sheet y devuelve
#  una lista de frames escalados
#  row       → que fila cortar (0-7)
#  frame_w/h → tamaño original de cada frame
#  frame_count → cuantos frames tiene la fila
# ─────────────────────────────────────────
def get_frames(sheet: pygame.Surface, row_index: int, frame_width: int, frame_height: int, frame_count: int, frame_scaled_w: int, frame_scaled_h: int) -> list:

    if not sheet:
        print("No Sprite Sheet Found")
        return []

    frames = []

    for column in range(frame_count):
        frame = sheet.subsurface(pygame.Rect(column * frame_width, row_index * frame_height, frame_width, frame_height))
        frame = pygame.transform.scale(frame, (frame_scaled_w, frame_scaled_h))
        frames.append(frame)
        
    return frames

# ─────────────────────────────────────────
#  draw()
#  Limpia la pantalla y dibuja el frame actual
#  del personaje en su posicion
# ─────────────────────────────────────────
def draw(window: pygame.Surface, animations: dict[str, list[pygame.Surface]], direction: str, frame_idx: int, pos: tuple[int, int]) -> None:
    window.fill((0, 0, 0))
    window.blit(animations[direction][frame_idx], pos)
    pygame.display.update()

# Character Selection Screen
def selection_screen(window):
    overlay_screen = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    overlay_screen.fill((0, 0, 0))
    # opcional: hacerlo semitransparente
    overlay_screen.set_alpha(200)      # 0=invisible, 255=opaco


# ───────────────────────────────────────────────────────────────────
# Movement Handler
# Mueve el personaje en la pantalla acorde con la teclas presionadas
# ───────────────────────────────────────────────────────────────────
def movement_handler(keys, direction, pos):
    x, y = pos
    diagonal_speed = 2 # Normalize the vector here since we dont have delta time implemented yet
    cardinal_speed = 3

    # Full 8 Directional Movement but not needed for now
    if keys[pygame.K_s] and keys[pygame.K_a]: y += diagonal_speed; x -= diagonal_speed; direction = "down-left"
    elif keys[pygame.K_s] and keys[pygame.K_d]: y += diagonal_speed; x += diagonal_speed; direction = 'down-right'
    elif keys[pygame.K_w] and keys[pygame.K_a]: y -= diagonal_speed; x -= diagonal_speed; direction = 'up-left'
    elif keys[pygame.K_w] and keys[pygame.K_d]: x += diagonal_speed; y -= diagonal_speed; direction = 'up-right'
    elif keys[pygame.K_a]: x -= cardinal_speed; direction = 'left'
    elif keys[pygame.K_d]: x += cardinal_speed; direction = 'right'
    elif keys[pygame.K_w]: y -= cardinal_speed; direction = 'up'
    elif keys[pygame.K_s]: y += cardinal_speed; direction = 'down'
    
    # ── Limites de pantalla ──
    x = max(0, min(x, WINDOW_WIDTH  - DISPLAY_W))
    y = max(0, min(y, WINDOW_HEIGHT - DISPLAY_H))

    return (x, y),  direction


# ─────────────────────────────────────────
#  main()
#  Game loop principal
# ─────────────────────────────────────────
def main():
    sprite_sheet = pygame.image.load(os.path.join(BASE_DIR, 'assets','Sprites','Pokemon Characters','Articuno','Walk-Anim.png' )).convert_alpha() # Load the Sprite Sheet once

    player_animations = {
        'left':  get_frames(sprite_sheet, DIRECTION_ROWS['left'],  FRAME_WIDTH, FRAME_HEIGHT, FRAME_COUNT, DISPLAY_W, DISPLAY_H),
        'right': get_frames(sprite_sheet, DIRECTION_ROWS['right'], FRAME_WIDTH, FRAME_HEIGHT, FRAME_COUNT, DISPLAY_W, DISPLAY_H),
        'up-right': get_frames(sprite_sheet, DIRECTION_ROWS['up-right'], FRAME_WIDTH, FRAME_HEIGHT, FRAME_COUNT, DISPLAY_W, DISPLAY_H),
        'up': get_frames(sprite_sheet, DIRECTION_ROWS['up'], FRAME_WIDTH, FRAME_HEIGHT, FRAME_COUNT, DISPLAY_W, DISPLAY_H),
        'down': get_frames(sprite_sheet, DIRECTION_ROWS['down'], FRAME_WIDTH, FRAME_HEIGHT, FRAME_COUNT, DISPLAY_W, DISPLAY_H),
        'down-right': get_frames(sprite_sheet, DIRECTION_ROWS['down-right'], FRAME_WIDTH, FRAME_HEIGHT, FRAME_COUNT, DISPLAY_W, DISPLAY_H),
        'down-left': get_frames(sprite_sheet, DIRECTION_ROWS['down-left'], FRAME_WIDTH, FRAME_HEIGHT, FRAME_COUNT, DISPLAY_W, DISPLAY_H),
        'up-left': get_frames(sprite_sheet, DIRECTION_ROWS['up-left'], FRAME_WIDTH, FRAME_HEIGHT, FRAME_COUNT, DISPLAY_W, DISPLAY_H),
    }

    """
    for direction, index in DIRECTION_ROWS.items():
        direction, index = get_frames()
    """
    x, y = (-WINDOW_WIDTH, WINDOW_HEIGHT // 2)

    frame_idx  = 0
    anim_timer = 0
    anim_speed = 6
    direction = 'right'
    running = True
    vel_y = 0
    moving = False

    while running:
        CLOCK.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                # Espacio impulsa hacia arriba (Flap)
                if event.key == pygame.K_SPACE:
                    vel_y = FLAP_FORCE

        keys = pygame.key.get_pressed()
        
        
        (x, y), direction = movement_handler(keys, direction, (x, y))

        moving = keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_w] or keys[pygame.K_s] # Moving state for later on

        # ── Fisica: aplicar gravedad ──
        vel_y += GRAVITY   # acumula velocidad hacia abajo
        y += vel_y         # aplica velocidad a la posicion
        if y >= WINDOW_HEIGHT - DISPLAY_H:
            y = WINDOW_HEIGHT - DISPLAY_H
            vel_y = 0


        # animacion
        anim_timer += 1
        if anim_timer > anim_speed:
            anim_timer = 0
            # moving: #-> Add if you need to animation to stay on frame 0 
            frame_idx = (frame_idx + 1) % FRAME_COUNT

        draw(WINDOW, player_animations, direction, frame_idx, (x, y))

    pygame.quit()
if __name__ == "__main__":
    main()
# src/game.py
import pygame
import os

# Pygame Window Config and Global Constants
# =============================================================
pygame.init()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WINDOW_WIDTH, WINDOW_HEIGHT = 1680, 820
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Lateral Movement Test')
CLOCK = pygame.time.Clock()
FPS = 60
# =============================================================


# Function in charge of building the frame array for each animation
# =============================================================
def get_frames(sprite_sheet: list[pygame.Surface],int, row: int, frame_width: int, frame_height: int, frame_display_w: int, frame_display_h: int, frame_count:int) -> list[pygame.Surface]:
    if not sprite_sheet:
        print("No Sprite Sheet Found")
        return []

    frames = []
    for column in range(frame_count):
        frame = sprite_sheet.Subsurface(pygame.Rect(
            column * frame_display_w,
            row * frame_height,
            frame_width,
            frame_height
        ))
        frames.append(frame)

    return frames
        

def draw():
    WINDOW.fill((0, 0, 0))
    WINDOW.blit()

def main() -> None:
    pass

if __name__ == "__main__":
    main()
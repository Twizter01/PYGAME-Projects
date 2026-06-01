""" Function in charge of dividing the sprite sheet
    into a given frame width and frame height and create an
    image of each new frame, this version allows you to run thru
    a matrix and have multiple animation states"""

# src/sprite_utils.py
import pygame

def get_frames(sheet, row, fw, fh, frame_count):
    FRAME_COUNT = 4
    frames = [] # Build an array of Rects with the frames for each animation
    for col in range(frame_count):
        frame = sheet.subsurface(pygame.Rect(col * fw, row * fh, fw, fw))
        frames.append(frame)
    return frames


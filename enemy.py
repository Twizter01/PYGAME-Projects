# src/enemy.py
import pygame
import math
import random
from src.sprite_utils import get_frames

DIRECTION_ROWS = {
    'down':       0,
    'down-left':  7,
    'left':       6,
    'up-left':    5,
    'up':         4,
    'up-right':   3,
    'right':      2,
    'down-right': 1,
}

class Enemy:
    FRAME_WIDTH          = 24
    FRAME_HEIGHT         = 48
    FRAME_COUNT          = 8
    FRAME_DISPLAY_WIDTH  = 96
    FRAME_DISPLAY_HEIGHT = 120

    def __init__(self, assets, window_width, window_height):
        self.window_width  = window_width
        self.window_height = window_height

        sheet = assets.get_sheet('assets/Sprites/Pokemon Characters/Misdreavus/Walk-Anim.png')
        self.anims = {
            d: get_frames(sheet, row, self.FRAME_WIDTH, self.FRAME_HEIGHT, self.FRAME_COUNT, self.FRAME_DISPLAY_WIDTH, self.FRAME_DISPLAY_HEIGHT)
            for d, row in DIRECTION_ROWS.items()
        }

        self.pos             = self._random_pos()
        self.direction       = 'down'
        self.frame_index     = 0
        self.animation_timer = 0
        self.animation_speed = 9
        self.speed           = 2
        self.catch_radius    = 60

    def _random_pos(self):
        x = random.randint(100, self.window_width  - 100 - self.FRAME_DISPLAY_WIDTH)
        y = random.randint(100, self.window_height - 100 - self.FRAME_DISPLAY_HEIGHT)
        return (float(x), float(y))

    def respawn(self):
        self.pos = self._random_pos()

    def get_rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.FRAME_DISPLAY_WIDTH, self.FRAME_DISPLAY_HEIGHT)

    def check_catch(self, player_pos):
        px, py = player_pos
        ex, ey = self.pos
        return math.sqrt((px - ex) ** 2 + (py - ey) ** 2) < self.catch_radius

    def update(self, player_pos, player_vel):
        self._move(player_pos, player_vel)
        self._animate()

    def _move(self, player_pos, player_vel):
        ex, ey = self.pos
        px, py = player_pos
        pvx, pvy = player_vel

        predicted_px = px + pvx * 30
        predicted_py = py + pvy * 30

        player_dx = px - ex
        player_dy = py - ey
        player_dist = math.sqrt(player_dx * player_dx + player_dy * player_dy)
        close_threshold = 260

        if player_dist < close_threshold:
            desired_dx = -player_dx
            desired_dy = -player_dy
            run_speed = self.speed * 2.2
        else:
            desired_dx = ex - predicted_px
            desired_dy = ey - predicted_py
            run_speed = self.speed

        dist = math.sqrt(desired_dx * desired_dx + desired_dy * desired_dy)
        if dist > 0:
            desired_dx = (desired_dx / dist) * run_speed
            desired_dy = (desired_dy / dist) * run_speed

        wall_dx = 0.0
        wall_dy = 0.0
        wall_margin = 140
        if ex < wall_margin:
            wall_dx += (wall_margin - ex)
        if ex > self.window_width - self.FRAME_DISPLAY_WIDTH - wall_margin:
            wall_dx -= (ex - (self.window_width - self.FRAME_DISPLAY_WIDTH - wall_margin))
        if ey < wall_margin:
            wall_dy += (wall_margin - ey)
        if ey > self.window_height - self.FRAME_DISPLAY_HEIGHT - wall_margin:
            wall_dy -= (ey - (self.window_height - self.FRAME_DISPLAY_HEIGHT - wall_margin))

        if wall_dx != 0 or wall_dy != 0:
            wdist = math.sqrt(wall_dx * wall_dx + wall_dy * wall_dy)
            wall_dx = (wall_dx / wdist) * run_speed
            wall_dy = (wall_dy / wdist) * run_speed

        center_dx = (self.window_width / 2) - ex
        center_dy = (self.window_height / 2) - ey
        center_dist = math.sqrt(center_dx * center_dx + center_dy * center_dy)
        if center_dist > 0:
            center_dx = (center_dx / center_dist) * run_speed
            center_dy = (center_dy / center_dist) * run_speed

        if player_dist < close_threshold:
            flee_weight = 0.75
            wall_weight = 0.2
            center_weight = 0.05
        else:
            flee_weight = 0.55
            wall_weight = 0.3
            center_weight = 0.15

        final_dx = desired_dx * flee_weight + wall_dx * wall_weight + center_dx * center_weight
        final_dy = desired_dy * flee_weight + wall_dy * wall_weight + center_dy * center_weight

        final_dist = math.sqrt(final_dx * final_dx + final_dy * final_dy)
        if final_dist > 0:
            final_dx = (final_dx / final_dist) * run_speed
            final_dy = (final_dy / final_dist) * run_speed

        ex = max(0, min(ex + final_dx, self.window_width  - self.FRAME_DISPLAY_WIDTH))
        ey = max(0, min(ey + final_dy, self.window_height - self.FRAME_DISPLAY_HEIGHT))
        self.pos = (ex, ey)

        new_dir = self._vector_to_direction(final_dx, final_dy)
        if new_dir:
            self.direction = new_dir

    def _vector_to_direction(self, dx, dy):
        if dx == 0 and dy == 0:
            return None
        angle = math.degrees(math.atan2(-dy, dx))
        if   angle >= 67.5   and angle < 112.5:  return 'up'
        elif angle >= 22.5   and angle < 67.5:   return 'up-right'
        elif angle >= -22.5  and angle < 22.5:   return 'right'
        elif angle >= -67.5  and angle < -22.5:  return 'down-right'
        elif angle >= -112.5 and angle < -67.5:  return 'down'
        elif angle >= -157.5 and angle < -112.5: return 'down-left'
        elif angle >= 112.5  and angle < 157.5:  return 'up-left'
        else:                                     return 'left'

    def _animate(self):
        self.animation_timer += 1
        if self.animation_timer > self.animation_speed:
            self.animation_timer = 0
            self.frame_index     = (self.frame_index + 1) % self.FRAME_COUNT

    def draw(self, window):
        window.blit(self.anims[self.direction][self.frame_index], self.pos)
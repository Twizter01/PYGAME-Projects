import math
import random
import pygame

class Ball:
    RADIUS = 10
    SPEED = 6

    def __init__(self, window_width, window_height):
        self.window_width = window_width
        self.window_height = window_height
        self.current_speed = self.SPEED
        self.reset()

    def reset(self):
        self.x = self.window_width / 2
        self.y = self.window_height / 2
        self.vx = random.choice((-1, 1)) * self.current_speed
        self.vy = random.uniform(-3.0, 3.0)

    def get_rect(self):
        return pygame.Rect(int(self.x - self.RADIUS), int(self.y - self.RADIUS), self.RADIUS * 2, self.RADIUS * 2)

    def update(self, player_paddle, enemy_paddle):
        self.x += self.vx
        self.y += self.vy

        if self.y - self.RADIUS <= 0:
            self.y = self.RADIUS
            self.vy = abs(self.vy)
        elif self.y + self.RADIUS >= self.window_height:
            self.y = self.window_height - self.RADIUS
            self.vy = -abs(self.vy)

        ball_rect = self.get_rect()
        if ball_rect.colliderect(player_paddle.get_rect()):
            self.x = player_paddle.x + player_paddle.width + self.RADIUS
            self.vx = abs(self.vx)
            self._add_spin(player_paddle)
        elif ball_rect.colliderect(enemy_paddle.get_rect()):
            self.x = enemy_paddle.x - self.RADIUS
            self.vx = -abs(self.vx)
            self._add_spin(enemy_paddle)

        if self.x < 0:
            return 'enemy'
        if self.x > self.window_width:
            return 'player'
        return None

    def _add_spin(self, paddle):
        offset = (self.y - paddle.y - paddle.height / 2) / (paddle.height / 2)
        self.vy += offset * 2.5
        self.vy = max(-7.5, min(self.vy, 7.5))
        self.vx = max(-9, min(self.vx, 9))

    def increase_speed(self, factor=1.1):
        self.current_speed *= factor
        self.current_speed = min(self.current_speed, 14)
        self.vx = math.copysign(min(abs(self.vx) * factor, 14), self.vx)
        self.vy = math.copysign(min(abs(self.vy) * factor, 12), self.vy)

    def draw(self, window):
        pygame.draw.circle(window, (255, 255, 255), (int(self.x), int(self.y)), self.RADIUS)

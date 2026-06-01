import pygame

class Paddle:
    WIDTH = 20
    HEIGHT = 100
    SPEED = 6

    def __init__(self, x, y, window_width, window_height, up_key=None, down_key=None, is_ai=False):
        self.x = x
        self.y = y
        self.window_width = window_width
        self.window_height = window_height
        self.up_key = up_key
        self.down_key = down_key
        self.is_ai = is_ai
        self.width = self.WIDTH
        self.height = self.HEIGHT

    def get_rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def update(self, keys, ball=None):
        dy = 0
        if self.is_ai and ball is not None:
            if ball.y < self.y + self.height * 0.4:
                dy = -self.SPEED
            elif ball.y > self.y + self.height * 0.6:
                dy = self.SPEED
        else:
            if self.up_key and keys[self.up_key]:
                dy = -self.SPEED
            if self.down_key and keys[self.down_key]:
                dy = self.SPEED

        self.y = max(0, min(self.window_height - self.height, self.y + dy))

    def draw(self, window):
        pygame.draw.rect(window, (255, 255, 255), self.get_rect())

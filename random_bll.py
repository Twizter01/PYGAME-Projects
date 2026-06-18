
"""
Snake 2003 — Java Phone Edition
Python/pygame port of the HTML canvas version.
Requires: pip install pygame
Run:      python snake_2003.py
"""

import pygame
import sys
import random

# ── Palette (Game Boy green) ─────────────────────────────────────
BG_COLOR    = (155, 188,  15)   # lightest green  (field tiles)
DARK_COLOR  = ( 15,  56,  15)   # darkest green   (HUD, head, food)
MID_COLOR   = ( 48,  98,  48)   # mid green       (body segments)
LIGHT_COLOR = (139, 172,  15)   # checker fill
HUD_TEXT    = (139, 172,  15)   # score / title text

# ── Phone shell colours ──────────────────────────────────────────
SHELL_COLOR  = ( 42,  42,  42)
BEZEL_COLOR  = ( 17,  17,  17)
KEY_COLOR    = ( 51,  51,  51)
KEY_PRESS    = ( 30,  30,  30)
KEY_DPAD     = ( 34,  34,  34)
KEY_CENTER   = ( 68,  68,  68)
KEY_TEXT     = (200, 200, 200)
SHADOW_COLOR = ( 17,  17,  17)

# ── Layout constants ─────────────────────────────────────────────
CELL      = 8          # pixels per grid cell
COLS      = 21         # game columns  (168 / 8)
ROWS      = 15         # game rows     (120 / 8)
SCREEN_W  = 168
SCREEN_H  = 140
HUD_H     = 20         # HUD bar height

# Phone shell dimensions
SHELL_W   = 260
SHELL_H   = 520
WIN_W     = SHELL_W + 40
WIN_H     = SHELL_H + 40

# Screen position inside the shell
SCREEN_X  = 20 + (SHELL_W - SCREEN_W) // 2   # centred
SCREEN_Y  = 60                                 # below speaker / brand


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


# ── Game state ───────────────────────────────────────────────────
class Game:
    def __init__(self):
        self.snake   = [(5, 5), (4, 5), (3, 5)]
        self.dir     = (1, 0)
        self.next_dir = (1, 0)
        self.food    = self._spawn_food()
        self.score   = 0
        self.speed   = 200    # ms per tick
        self.state   = 'start'   # 'start' | 'playing' | 'dead'
        self._tick_acc = 0

    def _spawn_food(self):
        while True:
            f = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
            if f not in self.snake:
                return f

    def start_new(self):
        self.snake    = [(5, 5), (4, 5), (3, 5)]
        self.dir      = (1, 0)
        self.next_dir = (1, 0)
        self.food     = self._spawn_food()
        self.score    = 0
        self.speed    = 200
        self.state    = 'playing'
        self._tick_acc = 0

    def set_dir(self, dx, dy):
        if self.state != 'playing':
            return
        # Prevent 180° reversal
        if (dx, dy) == (-self.dir[0], -self.dir[1]):
            return
        self.next_dir = (dx, dy)

    def update(self, dt_ms):
        if self.state != 'playing':
            return
        self._tick_acc += dt_ms
        if self._tick_acc < self.speed:
            return
        self._tick_acc -= self.speed

        self.dir = self.next_dir
        hx = self.snake[0][0] + self.dir[0]
        hy = self.snake[0][1] + self.dir[1]

        # Collision
        if (hx < 0 or hx >= COLS or hy < 0 or hy >= ROWS
                or (hx, hy) in self.snake):
            self.state = 'dead'
            return

        self.snake.insert(0, (hx, hy))

        if (hx, hy) == self.food:
            self.score += 1
            self.food = self._spawn_food()
            if self.score % 5 == 0 and self.speed > 80:
                self.speed = max(80, self.speed - 20)
        else:
            self.snake.pop()


# ── Renderer ─────────────────────────────────────────────────────
def draw_game_screen(surf, game, font_small, font_tiny):
    """Draw the 168×140 game canvas onto `surf`."""
    surf.fill(BG_COLOR)

    # HUD bar
    pygame.draw.rect(surf, DARK_COLOR, (0, 0, SCREEN_W, HUD_H))
    title = font_small.render('SNAKE', True, HUD_TEXT)
    surf.blit(title, (4, 4))
    score_txt = font_small.render(str(game.score), True, HUD_TEXT)
    surf.blit(score_txt, (SCREEN_W - score_txt.get_width() - 4, 4))
    pygame.draw.line(surf, MID_COLOR, (0, HUD_H), (SCREEN_W, HUD_H))

    OY = HUD_H  # y-offset for grid

    # Checkerboard
    for gx in range(COLS):
        for gy in range(ROWS):
            if (gx + gy) % 2 == 0:
                pygame.draw.rect(surf, LIGHT_COLOR,
                                 (gx * CELL, OY + gy * CELL, CELL, CELL))

    # Food
    fx, fy = game.food
    pygame.draw.rect(surf, DARK_COLOR,
                     (fx * CELL + 2, OY + fy * CELL + 1, CELL - 4, CELL - 2))
    pygame.draw.rect(surf, BG_COLOR,
                     (fx * CELL + 3, OY + fy * CELL + 2, 2, 2))  # highlight

    # Snake
    dx, dy = game.dir
    for i, (sx, sy) in enumerate(game.snake):
        color = DARK_COLOR if i == 0 else MID_COLOR
        pygame.draw.rect(surf, color,
                         (sx * CELL + 1, OY + sy * CELL + 1, CELL - 2, CELL - 2))
        if i == 0:  # eyes
            if dx != 0:
                pygame.draw.rect(surf, BG_COLOR,
                                 (sx * CELL + CELL - 4, OY + sy * CELL + 2, 2, 2))
                pygame.draw.rect(surf, BG_COLOR,
                                 (sx * CELL + CELL - 4, OY + sy * CELL + CELL - 4, 2, 2))
            else:
                pygame.draw.rect(surf, BG_COLOR,
                                 (sx * CELL + 2, OY + sy * CELL + CELL - 4, 2, 2))
                pygame.draw.rect(surf, BG_COLOR,
                                 (sx * CELL + CELL - 4, OY + sy * CELL + CELL - 4, 2, 2))

    # Overlays
    if game.state == 'dead':
        overlay = pygame.Surface((132, 60), pygame.SRCALPHA)
        overlay.fill((15, 56, 15, 209))
        surf.blit(overlay, (18, 45))
        pygame.draw.rect(surf, BG_COLOR, (19, 46, 130, 58), 1)
        go = font_small.render('GAME OVER', True, BG_COLOR)
        surf.blit(go, (SCREEN_W // 2 - go.get_width() // 2, 56))
        sc = font_small.render(f'SCORE: {game.score}', True, BG_COLOR)
        surf.blit(sc, (SCREEN_W // 2 - sc.get_width() // 2, 68))
        hint = font_tiny.render('ENTER = NEW GAME', True, BG_COLOR)
        surf.blit(hint, (SCREEN_W // 2 - hint.get_width() // 2, 82))

    if game.state == 'start':
        pygame.draw.rect(surf, DARK_COLOR, (0, 30, SCREEN_W, 80))
        pygame.draw.rect(surf, BG_COLOR, (8, 38, 152, 64), 1)
        title2 = font_small.render('SNAKE', True, BG_COLOR)
        surf.blit(title2, (SCREEN_W // 2 - title2.get_width() // 2, 50))
        ed = font_tiny.render('2003 EDITION', True, BG_COLOR)
        surf.blit(ed, (SCREEN_W // 2 - ed.get_width() // 2, 64))
        pr = font_tiny.render('PRESS ENTER', True, BG_COLOR)
        surf.blit(pr, (SCREEN_W // 2 - pr.get_width() // 2, 80))


def draw_phone(win, game_surf, press_state):
    """Draw the phone shell around the game canvas."""
    win.fill((26, 26, 26))

    ox = (WIN_W - SHELL_W) // 2
    oy = (WIN_H - SHELL_H) // 2

    # Shell body
    pygame.draw.rect(win, SHELL_COLOR, (ox, oy, SHELL_W, SHELL_H), border_radius=22)
    pygame.draw.rect(win, SHADOW_COLOR, (ox, oy, SHELL_W, SHELL_H), 2, border_radius=22)

    # Speaker dots
    dot_y = oy + 14
    for i in range(5):
        pygame.draw.circle(win, SHADOW_COLOR,
                           (ox + SHELL_W // 2 - 10 + i * 5, dot_y), 2)

    # Brand text  (we use a tiny pygame font — no TTF needed here)
    brand_font = pygame.font.SysFont('courier', 8, bold=True)
    brand = brand_font.render('JAVA PHONE', True, (85, 85, 85))
    win.blit(brand, (ox + SHELL_W // 2 - brand.get_width() // 2, oy + 24))

    # Screen bezel
    bx = ox + SCREEN_X - 8
    by = oy + SCREEN_Y - 6
    bw = SCREEN_W + 16
    bh = SCREEN_H + 12
    pygame.draw.rect(win, BEZEL_COLOR, (bx, by, bw, bh), border_radius=8)
    pygame.draw.rect(win, SHADOW_COLOR, (bx, by, bw, bh), 2, border_radius=8)

    # Game canvas
    win.blit(game_surf, (ox + SCREEN_X, oy + SCREEN_Y))

    # ── Soft keys + OK ──────────────────────────────────────────
    sk_y = oy + SCREEN_Y + SCREEN_H + 16
    key_h = 22

    def draw_key(rect, label, pressed=False, radius=5):
        col = KEY_PRESS if pressed else KEY_COLOR
        pygame.draw.rect(win, col, rect, border_radius=radius)
        if not pressed:
            shadow = pygame.Rect(rect.x, rect.y + key_h - 3, rect.w, 3)
            pygame.draw.rect(win, SHADOW_COLOR, shadow, border_radius=radius)
        kf = pygame.font.SysFont('courier', 7, bold=True)
        txt = kf.render(label, True, KEY_TEXT)
        win.blit(txt, (rect.centerx - txt.get_width() // 2,
                       rect.centery - txt.get_height() // 2))

    left_sk  = pygame.Rect(ox + 14,  sk_y, 54, key_h)
    ok_key   = pygame.Rect(ox + SHELL_W // 2 - 22, sk_y, 44, key_h)
    right_sk = pygame.Rect(ox + SHELL_W - 68, sk_y, 54, key_h)

    draw_key(left_sk,  'MENU',  press_state.get('menu', False))
    draw_key(ok_key,   'OK',    press_state.get('ok', False),  radius=5)
    draw_key(right_sk, 'BACK',  press_state.get('back', False))

    # ── D-pad ───────────────────────────────────────────────────
    dp_y   = sk_y + key_h + 10
    dp_cx  = ox + SHELL_W // 2
    dp_sz  = 28   # arrow key size
    dp_gap = 2

    up_rect    = pygame.Rect(dp_cx - dp_sz // 2, dp_y, dp_sz, dp_sz)
    down_rect  = pygame.Rect(dp_cx - dp_sz // 2, dp_y + dp_sz * 2 + dp_gap * 2, dp_sz, dp_sz)
    left_rect  = pygame.Rect(dp_cx - dp_sz * 3 // 2 - dp_gap, dp_y + dp_sz + dp_gap, dp_sz, dp_sz)
    right_rect = pygame.Rect(dp_cx + dp_sz // 2 + dp_gap, dp_y + dp_sz + dp_gap, dp_sz, dp_sz)
    center_r   = pygame.Rect(dp_cx - dp_sz // 2, dp_y + dp_sz + dp_gap, dp_sz, dp_sz)

    def draw_dpad_key(rect, label, pressed=False):
        col = KEY_PRESS if pressed else KEY_DPAD
        pygame.draw.rect(win, col, rect, border_radius=4)
        if not pressed:
            sh = pygame.Rect(rect.x, rect.bottom - 3, rect.w, 3)
            pygame.draw.rect(win, SHADOW_COLOR, sh, border_radius=4)
        af = pygame.font.SysFont('courier', 11, bold=True)
        atxt = af.render(label, True, (170, 170, 170))
        win.blit(atxt, (rect.centerx - atxt.get_width() // 2,
                        rect.centery - atxt.get_height() // 2))

    draw_dpad_key(up_rect,    '^', press_state.get('up', False))
    draw_dpad_key(down_rect,  'v', press_state.get('down', False))
    draw_dpad_key(left_rect,  '<', press_state.get('left', False))
    draw_dpad_key(right_rect, '>', press_state.get('right', False))
    pygame.draw.circle(win, (26, 26, 26), center_r.center, dp_sz // 2 - 2)

    # ── Number pad ─────────────────────────────────────────────
    num_y   = dp_y + dp_sz * 3 + dp_gap * 2 + 12
    num_labels = ['1','2','3','4','5','6','7','8','9','*','0','#']
    nk_w, nk_h = 46, 20
    nk_gap = 6

    for i, label in enumerate(num_labels):
        col_i = i % 3
        row_i = i // 3
        nx = ox + 14 + col_i * (nk_w + nk_gap)
        ny = num_y + row_i * (nk_h + nk_gap)
        r  = pygame.Rect(nx, ny, nk_w, nk_h)
        col = (45, 45, 45)
        pygame.draw.rect(win, col, r, border_radius=4)
        pygame.draw.rect(win, SHADOW_COLOR, pygame.Rect(nx, ny + nk_h - 3, nk_w, 3), border_radius=4)
        nf = pygame.font.SysFont('courier', 8, bold=True)
        nt = nf.render(label, True, KEY_TEXT)
        win.blit(nt, (r.centerx - nt.get_width() // 2, r.centery - nt.get_height() // 2))

    return {
        'up': up_rect, 'down': down_rect,
        'left': left_rect, 'right': right_rect,
        'ok': ok_key,
    }


# ── Main ─────────────────────────────────────────────────────────
def main():
    pygame.init()
    win = pygame.display.set_mode((WIN_W, WIN_H))
    pygame.display.set_caption('Snake 2003 — Java Phone Edition')
    clock = pygame.time.Clock()

    # Pixel fonts (fallback to courier if Press Start 2P not installed)
    try:
        font_small = pygame.font.Font(None, 14)   # pygame built-in bitmap font
        font_tiny  = pygame.font.Font(None, 12)
    except Exception:
        font_small = pygame.font.SysFont('courier', 9, bold=True)
        font_tiny  = pygame.font.SysFont('courier', 7, bold=True)

    game_surf  = pygame.Surface((SCREEN_W, SCREEN_H))
    game       = Game()

    press_state  = {}    # which keys are visually pressed
    press_timers = {}    # key → remaining ms for visual feedback

    KEY_PRESS_DURATION = 120  # ms

    running = True
    while running:
        dt = clock.tick(60)   # cap at 60 fps, get ms elapsed

        # Update visual key timers
        for k in list(press_timers):
            press_timers[k] -= dt
            if press_timers[k] <= 0:
                del press_timers[k]
                press_state.pop(k, None)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    press_state['ok'] = True
                    press_timers['ok'] = KEY_PRESS_DURATION
                    if game.state in ('dead', 'start'):
                        game.start_new()

                dirs = {
                    pygame.K_UP:    ('up',    0, -1),
                    pygame.K_DOWN:  ('down',  0,  1),
                    pygame.K_LEFT:  ('left', -1,  0),
                    pygame.K_RIGHT: ('right', 1,  0),
                }
                if event.key in dirs:
                    key_name, dx, dy = dirs[event.key]
                    press_state[key_name] = True
                    press_timers[key_name] = KEY_PRESS_DURATION
                    game.set_dir(dx, dy)

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                hit_rects = draw_phone.__dict__.get('_last_rects', {})
                for name, rect in hit_rects.items():
                    if rect.collidepoint(mx, my):
                        press_state[name] = True
                        press_timers[name] = KEY_PRESS_DURATION
                        if name == 'ok':
                            if game.state in ('dead', 'start'):
                                game.start_new()
                        elif name == 'up':    game.set_dir(0, -1)
                        elif name == 'down':  game.set_dir(0,  1)
                        elif name == 'left':  game.set_dir(-1, 0)
                        elif name == 'right': game.set_dir(1,  0)

        game.update(dt)

        draw_game_screen(game_surf, game, font_small, font_tiny)
        hit_rects = draw_phone(win, game_surf, press_state)
        draw_phone.__dict__['_last_rects'] = hit_rects

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()


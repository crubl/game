#GameField.py

import pygame as pg

# ==================== НАСТРОЙКИ ОТЛАДКИ ====================
SHOW_DEBUG_INFO = True    # Показывать FPS и координаты (True/False)
SHOW_GRID = True          # Показывать сетку на поле (True/False)
SHOW_WORLD_BORDERS = True # Показывать красные границы мира (True/False)

# ==================== НАСТРОЙКИ ПОЛЯ ====================
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
GAME_TITLE = "GameField test"

WORLD_WIDTH = 2400
WORLD_HEIGHT = 1800

WORLD_BORDER_LEFT = 0
WORLD_BORDER_RIGHT = WORLD_WIDTH
WORLD_BORDER_TOP = 0
WORLD_BORDER_BOTTOM = WORLD_HEIGHT

COLOR_BACKGROUND = (34, 139, 34)
COLOR_GRID = (0, 0, 0, 100)
COLOR_PLAYER = (0, 200, 255)

# ==================== НАСТРОЙКИ КАМЕРЫ ====================
CAMERA_DEADZONE_X = SCREEN_WIDTH // 4
CAMERA_DEADZONE_Y = SCREEN_HEIGHT // 4

# ==================== НАСТРОЙКИ ИГРОКА ====================
PLAYER_SIZE = 24
PLAYER_SPEED = 300

#======================== Камера ===========================
class Camera:
    def __init__(self, width: int, height: int, world_width: int, world_height: int):
        self.width = width
        self.height = height
        self.world_width = world_width
        self.world_height = world_height
        self.x = 0.0
        self.y = 0.0

    def update(self, target_x: float, target_y: float):
        target_cam_x = target_x - self.width // 2
        target_cam_y = target_y - self.height // 2
        self.x = target_cam_x
        self.y = target_cam_y
        max_x = max(0, self.world_width - self.width)
        max_y = max(0, self.world_height - self.height)
        self.x = max(0.0, min(self.x, float(max_x)))
        self.y = max(0.0, min(self.y, float(max_y)))

    def apply(self, pos):
        return (pos[0] - self.x, pos[1] - self.y)

    def apply_rect(self, rect):
        return pg.Rect(
            rect.x - int(self.x),
            rect.y - int(self.y),
            rect.width,
            rect.height
        )

#======================= Игрок (заглушка) ====================
class PlayerStub:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.size = PLAYER_SIZE
        self.speed = PLAYER_SPEED

    def update(self, dt: float, keys_pressed):
        move_x = 0
        move_y = 0

        if keys_pressed[pg.K_LEFT] or keys_pressed[pg.K_a]:
            move_x = -1
        if keys_pressed[pg.K_RIGHT] or keys_pressed[pg.K_d]:
            move_x = 1
        if keys_pressed[pg.K_UP] or keys_pressed[pg.K_w]:
            move_y = -1
        if keys_pressed[pg.K_DOWN] or keys_pressed[pg.K_s]:
            move_y = 1

        if move_x != 0 and move_y != 0:
            move_x *= 0.707
            move_y *= 0.707

        self.x += move_x * self.speed * dt
        self.y += move_y * self.speed * dt

        min_x = WORLD_BORDER_LEFT + self.size // 2
        max_x = WORLD_BORDER_RIGHT - self.size // 2
        min_y = WORLD_BORDER_TOP + self.size // 2
        max_y = WORLD_BORDER_BOTTOM - self.size // 2
        self.x = max(float(min_x), min(self.x, float(max_x)))
        self.y = max(float(min_y), min(self.y, float(max_y)))

    def get_rect(self):
        return pg.Rect(
            self.x - self.size // 2,
            self.y - self.size // 2,
            self.size,
            self.size
        )

    def draw(self, screen, camera):
        screen_rect = camera.apply_rect(self.get_rect())
        pg.draw.rect(screen, COLOR_PLAYER, screen_rect)
        center_screen = camera.apply((self.x, self.y))
        pg.draw.circle(screen, (255, 255, 255),
                       (int(center_screen[0]), int(center_screen[1])), 4)

#============================= Игровое поле ============================
class GameField:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pg.time.Clock()
        self.running = True

        self.player = PlayerStub(WORLD_WIDTH // 2, WORLD_HEIGHT // 2)
        self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT, WORLD_WIDTH, WORLD_HEIGHT)
        self.font = pg.font.Font(None, 24)

    def draw_grid(self):
        """Рисует сетку на поле"""
        grid_size = 64
        grid_surface = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pg.SRCALPHA)

        left = int(self.camera.x)
        top = int(self.camera.y)
        right = left + SCREEN_WIDTH
        bottom = top + SCREEN_HEIGHT

        start_x = (left // grid_size) * grid_size
        start_y = (top // grid_size) * grid_size

        x = start_x
        while x < right:
            screen_x = x - left
            pg.draw.line(grid_surface, COLOR_GRID,
                         (screen_x, 0), (screen_x, SCREEN_HEIGHT), 1)
            x += grid_size

        y = start_y
        while y < bottom:
            screen_y = y - top
            pg.draw.line(grid_surface, COLOR_GRID,
                         (0, screen_y), (SCREEN_WIDTH, screen_y), 1)
            y += grid_size

        self.screen.blit(grid_surface, (0, 0))

    def draw_debug_info(self):
        """Отображает отладочную информацию"""
        fps = self.clock.get_fps()
        info_lines = [
            f"FPS: {fps:.0f}",
            f"Игрок: ({int(self.player.x)}, {int(self.player.y)})",
            f"Камера: ({int(self.camera.x)}, {int(self.camera.y)})",
            f"Мир: {WORLD_WIDTH}x{WORLD_HEIGHT}",
            f"Управление: WASD / Стрелки"
        ]

        y_offset = 10
        for line in info_lines:
            text = self.font.render(line, True, (255, 255, 255))
            text_bg = pg.Surface((text.get_width() + 4, text.get_height() + 4))
            text_bg.fill((0, 0, 0))
            text_bg.set_alpha(180)
            self.screen.blit(text_bg, (6, y_offset - 2))
            self.screen.blit(text, (8, y_offset))
            y_offset += 22

    def handle_events(self):
        global SHOW_DEBUG_INFO, SHOW_GRID, SHOW_WORLD_BORDERS

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.running = False
                # Горячие клавиши для отладки
                elif event.key == pg.K_F1:  # F1 — дебаг инфо
                    SHOW_DEBUG_INFO = not SHOW_DEBUG_INFO
                elif event.key == pg.K_F2:  # F2 — сетка
                    SHOW_GRID = not SHOW_GRID
                elif event.key == pg.K_F3:  # F3 — границы
                    SHOW_WORLD_BORDERS = not SHOW_WORLD_BORDERS

    def update(self, dt: float):
        keys = pg.key.get_pressed()
        self.player.update(dt, keys)
        self.camera.update(self.player.x, self.player.y)

    def draw(self):
        """Отрисовывает всё игровое поле"""
        self.screen.fill(COLOR_BACKGROUND)

        # Сетка (только если включена)
        if SHOW_GRID:
            self.draw_grid()

        self.player.draw(self.screen, self.camera)

        # Отображать границы мира (можно включить и выключить в настройках)
        if SHOW_WORLD_BORDERS:
            if self.camera.x <= 0:
                pg.draw.rect(self.screen, (255, 50, 50), (0, 0, 5, SCREEN_HEIGHT))
            if self.camera.x + SCREEN_WIDTH >= WORLD_WIDTH:
                pg.draw.rect(self.screen, (255, 50, 50), (SCREEN_WIDTH - 5, 0, 5, SCREEN_HEIGHT))
            if self.camera.y <= 0:
                pg.draw.rect(self.screen, (255, 50, 50), (0, 0, SCREEN_WIDTH, 5))
            if self.camera.y + SCREEN_HEIGHT >= WORLD_HEIGHT:
                pg.draw.rect(self.screen, (255, 50, 50), (0, SCREEN_HEIGHT - 5, SCREEN_WIDTH, 5))

        # Отладочная информация (можно включить и выключить в настройках)
        if SHOW_DEBUG_INFO:
            self.draw_debug_info()

    def run(self):
        dt = 0.0
        while self.running:
            self.handle_events()
            self.update(dt)
            self.draw()
            pg.display.flip()
            dt = self.clock.tick(60) / 1000.0
        pg.quit()


if __name__ == "__main__":
    pg.init()
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption(GAME_TITLE)
    game = GameField(screen)
    game.run()
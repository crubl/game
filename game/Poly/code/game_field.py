import pygame as pg
import random
import os
from .camera import Camera

# ==================== НАСТРОЙКИ МИРА ====================
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
WORLD_WIDTH = 2400
WORLD_HEIGHT = 1800
COLOR_BACKGROUND = (20, 30, 20)      # тёмно-зелёный фон (Если спрайт не загрузился)

# ==================== НАСТРОЙКИ ЗЕМЛИ ====================
GROUND_SPRITE_PATH = "./Poly/sprites/ground.webp"  # путь к спрайту земли

# ==================== НАСТРОЙКИ ОТЛАДКИ ====================
SHOW_GRID = True        # показывать сетку
SHOW_DEBUG = True       # показывать отладочную информацию

# ==================== НАСТРОЙКИ СПАВНА ВРАГОВ ====================
SPAWN_DELAY = 5.0       # секунды между спавном врагов
MAX_ENEMIES = 10       # максимальное количество врагов на поле


class GameField:
    """Игровое поле — управляет камерой, игроком, врагами и спавном"""
    
    def __init__(self, screen):
        self.screen = screen
        self.clock = pg.time.Clock()
        self.running = True
        
        # Размеры мира
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.world_width = WORLD_WIDTH
        self.world_height = WORLD_HEIGHT
        self.color_bg = COLOR_BACKGROUND
        
        # ==================== ЗАГРУЗКА ЗЕМЛИ ====================
        self.ground_sprite = None
        self.tile_width = 0
        self.tile_height = 0
        self.load_ground_sprite()
        
        # Камера
        self.camera = Camera(
            self.screen_width, self.screen_height,
            self.world_width, self.world_height
        )
        
        # Игрок и враги
        self.player = None
        self.enemies = []
        
        # Настройки спавна
        self.spawn_timer = 0
        self.spawn_delay = SPAWN_DELAY
        self.max_enemies = MAX_ENEMIES
        
        # Отладка
        self.font = pg.font.Font(None, 24)
        self.show_grid = SHOW_GRID
        self.show_debug = SHOW_DEBUG
    
    def load_ground_sprite(self):
        """Загружает спрайт земли"""
        try:
            # Проверяем, существует ли файл
            if os.path.exists(GROUND_SPRITE_PATH):
                self.ground_sprite = pg.image.load(GROUND_SPRITE_PATH).convert_alpha()
                self.tile_width = self.ground_sprite.get_width()
                self.tile_height = self.ground_sprite.get_height()
                print(f"Земля загружена: {GROUND_SPRITE_PATH} ({self.tile_width}x{self.tile_height})")
            else:
                print(f"ВНИМАНИЕ: Спрайт земли не найден по пути {GROUND_SPRITE_PATH}")
                self.ground_sprite = None
        except Exception as e:
            print(f"Ошибка загрузки земли: {e}")
            self.ground_sprite = None
    
    def draw_ground(self):
        """Рисует землю с учётом камеры"""
        # Если спрайт не загружен — заливаем цветом
        if self.ground_sprite is None:
            self.screen.fill(self.color_bg)
            return
        
        # Вычисляем видимую область мира
        start_x = int(self.camera.x // self.tile_width) * self.tile_width
        start_y = int(self.camera.y // self.tile_height) * self.tile_height
        end_x = self.camera.x + self.screen_width
        end_y = self.camera.y + self.screen_height
        
        # Отрисовываем только видимые тайлы
        x = start_x
        while x < end_x:
            y = start_y
            while y < end_y:
                # Преобразуем мировые координаты в экранные
                screen_x = x - self.camera.x
                screen_y = y - self.camera.y
                self.screen.blit(self.ground_sprite, (screen_x, screen_y))
                y += self.tile_height
            x += self.tile_width
    
    def set_player(self, player):
        """Устанавливает игрока, за которым следит камера"""
        self.player = player
    
    def spawn_enemy(self):
        """Создаёт врага за пределами экрана"""
        if len(self.enemies) >= self.max_enemies:
            return
        
        from Characters.code.units.enemies.walker import Walker
        
        side = random.randint(0, 3)
        
        if side == 0:      # сверху
            x = random.randint(0, self.world_width)
            y = -50
        elif side == 1:    # снизу
            x = random.randint(0, self.world_width)
            y = self.world_height + 50
        elif side == 2:    # слева
            x = -50
            y = random.randint(0, self.world_height)
        else:              # справа
            x = self.world_width + 50
            y = random.randint(0, self.world_height)
        
        enemy = Walker(x, y, self.player, self.screen)
        self.enemies.append(enemy)
    
    def update(self, dt):
        """Обновляет состояние всех объектов"""
        if self.player:
            self.player.update(dt)
            self.camera.update(self.player.x, self.player.y)
            
            self.spawn_timer += dt
            if self.spawn_timer >= self.spawn_delay:
                self.spawn_timer = 0
                self.spawn_enemy()
            
            for enemy in self.enemies[:]:
                enemy.update(dt)
                if enemy.health <= 0:
                    self.enemies.remove(enemy)
    
    def draw_grid(self):
        """Рисует сетку для ориентира по полю"""
        grid_size = 64
        grid_surface = pg.Surface((self.screen_width, self.screen_height), pg.SRCALPHA)
        
        left = int(self.camera.x)
        top = int(self.camera.y)
        right = left + self.screen_width
        bottom = top + self.screen_height
        
        start_x = (left // grid_size) * grid_size
        start_y = (top // grid_size) * grid_size
        
        x = start_x
        while x < right:
            screen_x = x - left
            pg.draw.line(grid_surface, (0, 0, 0, 80), 
                        (screen_x, 0), (screen_x, self.screen_height), 1)
            x += grid_size
        
        y = start_y
        while y < bottom:
            screen_y = y - top
            pg.draw.line(grid_surface, (0, 0, 0, 80),
                        (0, screen_y), (self.screen_width, screen_y), 1)
            y += grid_size
        
        self.screen.blit(grid_surface, (0, 0))
    
    def draw_debug(self):
        """Отображает отладочную информацию на экране"""
        if not self.player:
            return
            
        fps = self.clock.get_fps()
        lines = [
            f"FPS: {fps:.0f}",
            f"Игрок: ({int(self.player.x)}, {int(self.player.y)})",
            f"Камера: ({int(self.camera.x)}, {int(self.camera.y)})",
            f"Врагов: {len(self.enemies)}/{self.max_enemies}",
            "F1 - отладка, F2 - сетка, ESC - выход"
        ]
        
        y = 10
        for line in lines:
            text = self.font.render(line, True, (255, 255, 255))
            text_bg = pg.Surface((text.get_width() + 8, text.get_height() + 4))
            text_bg.fill((0, 0, 0))
            text_bg.set_alpha(180)
            self.screen.blit(text_bg, (6, y - 2))
            self.screen.blit(text, (10, y))
            y += 22
    
    def draw(self):
        """Отрисовывает всё игровое поле"""
        # Рисуем землю (фон)
        self.draw_ground()
        
        # Сетка (поверх земли)
        if self.show_grid:
            self.draw_grid()
        
        # Враги (только видимые камерой)
        for enemy in self.enemies:
            if self.camera.is_visible(enemy.x, enemy.y):
                enemy.draw(self.screen, self.camera)
        
        # Игрок
        if self.player:
            self.player.draw(self.screen, self.camera)
        
        # Отладка
        if self.show_debug:
            self.draw_debug()
        
        pg.display.flip()
    
    def handle_events(self):
        """Обработка событий (клавиши, закрытие окна)"""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.running = False
                elif event.key == pg.K_F1:
                    self.show_debug = not self.show_debug
                elif event.key == pg.K_F2:
                    self.show_grid = not self.show_grid
    
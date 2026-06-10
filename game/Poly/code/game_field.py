import pygame as pg
import random
from constans import *
from .camera import Camera
from Characters.code.units.enemies.walker import Walker

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
        
        # ==================== Загрузка земли ====================
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
        
    def load_ground_sprite(self):
        """Загружает спрайт земли"""
        self.ground_sprite = pg.image.load(GROUND_SPRITE_PATH).convert_alpha()
        self.tile_width = self.ground_sprite.get_width()
        self.tile_height = self.ground_sprite.get_height()
        print(f"Земля загружена: {GROUND_SPRITE_PATH} ({self.tile_width}x{self.tile_height})")
            
    
    def draw_ground(self):
        """Рисует землю с учётом камеры"""
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
    
    def clampInterval(self, center, minVal, maxVal, offset=300):
            low = int(max(minVal, center - offset))
            high = int(min(maxVal, center + offset))
            if low > high:
                low = high = int(center)
            return low, high
    
    def spawn_enemy(self):
        """Создаёт врага за пределами экрана"""
        if len(self.enemies) >= self.max_enemies:
            return

        side = random.randint(0, 3)
        
        if side == 0: # сверху
            xMin, xMax = self.clampInterval(self.player.x, 0, self.world_width)
            x = random.randint(xMin, xMax)
            y = -50
        elif side == 1:# снизу
            xMin, xMax = self.clampInterval(self.player.x, 0, self.world_width)
            x = random.randint(xMin, xMax)
            y = self.world_height + 50
        elif side == 2:# слева
            x = -50
            yMin, yMax = self.clampInterval(self.player.y, 0, self.world_height)
            y = random.randint(yMin, yMax)
        else:# справа
            x = self.world_width + 50
            yMin, yMax = self.clampInterval(self.player.y, 0, self.world_height)
            y = random.randint(yMin, yMax)
        
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
    
    def draw(self):
        """Отрисовывает всё игровое поле"""
        # Рисуем землю (фон)
        self.draw_ground()
        
        # Враги (только видимые камерой)
        for enemy in self.enemies:
            if self.camera.is_visible(enemy.x, enemy.y):
                enemy.draw(self.screen, self.camera)
        
        # Игрок
        if self.player:
            self.player.draw(self.screen, self.camera)
        
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
    
from Characters.code.units.baseUnit import Unit
import pygame as pg

# ==================== НЕ БОЕВЫЕ СТАТЫ ====================
PLAYER_SPEED = 300          # скорость передвижения (пикселей/сек)
PLAYER_HEALTH = 750         # максимальное здоровье

# ==================== БОЕВЫЕ СТАТЫ =======================
PLAYER_DAMAGE = 150         # базовый урон

# ==================== ПАРАМЕТРЫ СПРАЙТА ==================
SPRITE_PATH = "./Characters/sprites/hero/hero.png"


class Warrior(Unit):
    
    def __init__(self, x, y, screen, game_field):
        super().__init__(x, y)
        self.screen = screen
        self.image = pg.image.load(SPRITE_PATH)    
        self.rect = self.image.get_rect()
        self.game_field = game_field
        
        # ==================== КООРДИНАТЫ ====================
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        
        # ==================== ХАРАКТЕРИСТИКИ ====================
        self.health = PLAYER_HEALTH
        self.speed = PLAYER_SPEED
        self.damage = PLAYER_DAMAGE
        self.size = self.image.get_width()
    
    def update(self, dt):
        """Обновление игрока каждый кадр"""
        self.move(dt)
    
    def death(self):
        """Смерть игрока — пока заглушка"""
        pass
    
    def move(self, dt):
        """Движение игрока (WASD или стрелки)"""
        keys = pg.key.get_pressed()
        move_x = 0
        move_y = 0
        
        # Обработка нажатий
        if keys[pg.K_w] or keys[pg.K_UP]:
            move_y -= 1
        if keys[pg.K_s] or keys[pg.K_DOWN]:
            move_y += 1
        if keys[pg.K_a] or keys[pg.K_LEFT]:
            move_x -= 1
        if keys[pg.K_d] or keys[pg.K_RIGHT]:
            move_x += 1
        
        # Нормализация диагонального движения (чтобы скорость была одинаковой)
        if move_x != 0 and move_y != 0:
            move_x *= 0.707
            move_y *= 0.707
        
        # Применяем движение
        self.x += move_x * self.speed * dt
        self.y += move_y * self.speed * dt
        
        # Ограничиваем границами мира
        self.x = max(20, min(self.x, self.game_field.world_width - 20))
        self.y = max(20, min(self.y, self.game_field.world_height - 20))
        
        # Обновляем rect для коллизий
        self.rect.x = self.x
        self.rect.y = self.y
    
    def draw(self, screen, camera):
        """Отрисовка игрока с учётом камеры"""
        # Получаем экранные координаты
        screen_pos = camera.apply(self.x, self.y)
        
        # Центрируем спрайт по его центру
        draw_x = screen_pos[0] - self.image.get_width() // 2
        draw_y = screen_pos[1] - self.image.get_height() // 2
        
        screen.blit(self.image, (draw_x, draw_y))
        
        # ==================== ПОЛОСКА ЗДОРОВЬЯ ====================
        bar_width = 40
        bar_height = 6
        health_percent = self.health / PLAYER_HEALTH
        bar_x = screen_pos[0] - bar_width // 2
        bar_y = screen_pos[1] - self.image.get_height() // 2 - 10
        
        # Фон полоски
        pg.draw.rect(screen, (60, 60, 60), (bar_x, bar_y, bar_width, bar_height))
        # Здоровье
        pg.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, bar_width * health_percent, bar_height))
        
        # ==================== ОТЛАДОЧНЫЙ КРУЖОК ====================
        # Показывает центр игрока (для проверки камеры)
        pg.draw.circle(screen, (255, 255, 255), 
                      (int(screen_pos[0]), int(screen_pos[1])), 3)
    
    def get_rect(self):
        """Возвращает прямоугольник для коллизий"""
        return pg.Rect(self.x - self.size//2, self.y - self.size//2, self.size, self.size)
    
    def getDamage(self):
        """Получение урона от врагов"""
        damage = self.damageMod()
        self.health -= damage
        if self.health <= 0:
            self.death()
        return damage
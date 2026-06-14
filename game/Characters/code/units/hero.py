from Characters.code.units.baseUnit import Unit
from constans import *
import pygame as pg
import random as rd


class Warrior(Unit):
    
    def __init__(self, x, y, screen, game_field):
        super().__init__(x, y)
        self.screen = screen
        self.image = pg.image.load(SPRITE_PATH).convert_alpha()   
        self.mask = pg.mask.from_surface(self.image)  
        self.radius = 25
        self.rect = self.image.get_rect(center=(x, y))
        self.game_field = game_field
        
        # ==================== Координаты ====================
        self.x = x
        self.y = y

        # ==================== Характеристики ====================
        self.level = 1
        self.maxHealth = 750
        self.health = self.maxHealth
        self.speed = 300
        self.radiusExp = 10
        self.damage = 100
        self.critChance = 0.05      # шанс крита (5%)
        self.critMod = 1.5          # множитель крита (150%)

        # ==================== Спрайт ====================
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
        self.rect.center = (self.x, self.y)
    
    def draw(self, screen, camera):
        """Отрисовка игрока с учётом камеры"""
        # Получаем экранные координаты
        screen_pos = camera.apply(self.x, self.y)
        
        # Центрируем спрайт по его центру
        draw_x = screen_pos[0] - self.image.get_width() // 2
        draw_y = screen_pos[1] - self.image.get_height() // 2
        
        screen.blit(self.image, (draw_x, draw_y))
        
        # ==================== Полоска здоровья ====================
        bar_width = 40
        bar_height = 6
        health_percent = self.health / self.maxHealth
        bar_x = screen_pos[0] - bar_width // 2
        bar_y = screen_pos[1] - self.image.get_height() // 2 - 10
        
        # Фон полоски
        pg.draw.rect(screen, (60, 60, 60), (bar_x, bar_y, bar_width, bar_height))
        # Здоровье
        pg.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, bar_width * health_percent, bar_height))
    
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
    
    def damageMod(self):
        """Расчёт урона с учётом шанса крита"""
        isCritDamage = rd.random() < self.critChance
        if isCritDamage:
            return self.damage * self.critMod
        else:
            return self.damage
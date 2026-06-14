from Characters.code.units.baseUnit import Unit
from constans import *
import pygame as pg
import math

class Walker(Unit):
    
    def __init__(self, x, y, hero, screen):
        super().__init__(x, y)
        self.hero = hero      # ссылка на игрока (нужна для ИИ)
        self.screen = screen

        # ==================== Спрайт ====================
        self.image = pg.image.load(SPRITE_PATH).convert_alpha()   
        self.mask = pg.mask.from_surface(self.image)  
        self.rect = self.image.get_rect(center=(x, y))
        
        # ==================== Характеристики ====================
        self.maxHealth = 1500
        self.health = self.maxHealth
        self.speed = 150
        self.damage = 80
    
    def update(self, dt):
        """Обновление врага каждый кадр"""
        self.move(dt)
    
    def death(self):
        """Смерть врага (пока заглушка)"""
        pass
    
    def collidesWith(self, other):
        # Сначала быстрая проверка по прямоугольникам (оптимизация)
        if not self.rect.colliderect(other.rect):
            return False
        
        # Точная проверка по маскам
        offsetX = other.rect.x - self.rect.x
        offsetY = other.rect.y - self.rect.y
        return self.mask.overlap(other.mask, (offsetX, offsetY)) is not None


    def move(self, dt):
        """Движение к игроку (простое ИИ)"""
        # Вектор к игроку
        dx = self.hero.x - self.x
        dy = self.hero.y - self.y
        distance = math.hypot(dx, dy)
        
        # Движение в сторону игрока
        if distance > 1:  # чтобы не делить на ноль
            dx /= distance
            dy /= distance
            self.x += dx * self.speed * dt
            self.y += dy * self.speed * dt
        self.rect.center = (self.x, self.y)
        
    def draw(self, screen, camera):
        """Отрисовка врага с учётом камеры"""
        # Получаем экранные координаты
        screen_pos = camera.apply(self.x, self.y)
        
        # Центрируем спрайт
        draw_x = screen_pos[0] - self.image.get_width() // 2
        draw_y = screen_pos[1] - self.image.get_height() // 2
        screen.blit(self.image, (draw_x, draw_y))
        
    def getDamage(self):
        """Получение урона от игрока"""
        damage = self.hero.damageMod()
        self.health -= damage
        if self.health <= 0:
            self.death()
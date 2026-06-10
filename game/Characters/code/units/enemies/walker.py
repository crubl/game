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
        self.image = pg.image.load(SPRITE_PATH)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # ==================== Характеристики ====================
        self.maxHealth = 50
        self.health = self.maxHealth
        self.speed = 150
        self.damage = 80
    
    def update(self, dt):
        """Обновление врага каждый кадр"""
        self.move(dt)
        self.rect.x = self.x
        self.rect.y = self.y
    
    def death(self):
        """Смерть врага (пока заглушка)"""
        pass
    
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
    
    def draw(self, screen, camera):
        """Отрисовка врага с учётом камеры"""
        # Получаем экранные координаты
        screen_pos = camera.apply(self.x, self.y)
        
        # Центрируем спрайт
        draw_x = screen_pos[0] - self.image.get_width() // 2
        draw_y = screen_pos[1] - self.image.get_height() // 2
        screen.blit(self.image, (draw_x, draw_y))
        
        # ==================== ПОЛОСКА ЗДОРОВЬЯ ====================
        bar_width = 30
        bar_height = 4
        health_percent = self.health / self.maxHealth
        bar_x = screen_pos[0] - bar_width // 2
        bar_y = screen_pos[1] - self.image.get_height() // 2 - 6
        
        # Фон полоски
        pg.draw.rect(screen, (60, 60, 60), (bar_x, bar_y, bar_width, bar_height))
        # Здоровье
        pg.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width * health_percent, bar_height))
    
    def getDamage(self):
        """Получение урона от игрока"""
        damage = self.damageMod()
        self.health -= damage
        if self.health <= 0:
            self.death()
        return damage

    # def getPosition(self):
    #     return (self.x, self.y)

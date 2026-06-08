from abc import ABC, abstractmethod
import random as rd
import pygame as pg


class Unit(pg.sprite.Sprite, ABC):
    """Абстрактный базовый класс для всех юнитов (игрок, враги)"""
    
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.rect = None
        self.image = None
        
        # Координаты (нужны для камеры)
        self.x = x
        self.y = y
        
        # ==================== ХАРАКТЕРИСТИКИ ====================
        self.level = 1          # уровень юнита
        self.health = 100       # текущее здоровье
        self.speed = 50         # скорость передвижения (пикселей/сек)
        
        # ==================== БОЕВЫЕ ХАРАКТЕРИСТИКИ ====================
        self.damage = 25            # базовый урон
        self.critChance = 0.05      # шанс крита (5%)
        self.critMod = 1.5          # множитель крита (150%)

    @abstractmethod
    def update(self, dt):
        """Обновление состояния юнита"""
        pass

    @abstractmethod
    def death(self):
        """Обработка смерти юнита"""
        pass

    @abstractmethod
    def move(self, dt):
        """Логика движения юнита"""
        pass

    def getDamage(self):
        """Получение урона юнитом"""
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
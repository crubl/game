from Characters.code.units.baseUnit import Unit
import pygame as pg
import math

class Walker(Unit):
    def __init__(self, x, y, hero, screen):
        #Наследуемые координаты из абстрактного класса Unit
        super().__init__(x, y)
        self.hero = hero
        #Параметры по умолчанию
        #Параметры спрайта
        self.screen = screen
        self.image = pg.image.load("./Characters/sprites/enemies/spritepaint.png")
        self.rect = self.image.get_rect()
        self.rect.x = self.hero.rect.x + 500
        self.rect.y = self.hero.rect.y + 500

        #Не боевые характиристики
        self.health = 750
        self.speed = 50

        #боевые статы
        self.damage = 20

    def update(self, dt):
        self.move(dt)

    def death(self): #смерть
        pass

    def move(self, dt): #движение юнита в зависимости от вида
        
        dx = self.hero.rect.centerx - self.rect.centerx
        dy = self.hero.rect.centery - self.rect.centery
        distance = math.hypot(dx, dy)

        if distance > 1:               # чтобы не делить на ноль
            dx /= distance
            dy /= distance
            self.rect.x += dx * self.speed * dt
            self.rect.y += dy * self.speed * dt
            
        
        self.x, self.y = self.rect.x, self.rect.y

    def getDamage(self): #получение урона

        damage = self.damageMod()
        self.health -= damage

        if self.health <= 0:
            self.death()
        
        return damage

    # def getPosition(self):
    #     return (self.x, self.y)

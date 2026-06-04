from .baseUnit import Unit
import pygame as pg


class Warrior(Unit):
    def __init__(self, x, y, screen):
        #Наследуемые координаты из абстрактного класса Unit
        super().__init__(x, y)

        #Параметры по умолчанию
        #Параметры спрайта
        self.screen = screen
        self.image = pg.image.load("./Characters/sprites/hero/hero.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        #Не боевые характиристики
        self.health = 750
        self.speed = 100

        #боевые статы
        self.damage = 150

    def update(self, dt):
        self.move(dt)

    def death(self): #смерть
        pass

    def move(self, dt): #движение юнита в зависимости от вида
        keys = pg.key.get_pressed()
        x, y = 0, 0
        if keys[pg.K_w]:
            y -= 1
        if keys[pg.K_s]:
            y += 1
        if keys[pg.K_a]:
            x -= 1
        if keys[pg.K_d]:
            x += 1
        
        self.rect.x += x * self.speed * dt
        self.rect.y += y * self.speed * dt
        
        self.x, self.y = self.rect.x, self.rect.y

    def getDamage(self): #получение урона

        damage = self.damageMod()
        self.health -= damage

        if self.health <= 0:
            self.death()
        
        return damage

    # def getPosition(self):
    #     return (self.x, self.y)

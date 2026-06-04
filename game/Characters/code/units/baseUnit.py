from abc import ABC, abstractmethod
import random as rd
import pygame as pg


class Unit(pg.sprite.Sprite, ABC):
    #Координаты создания
    def __init__(self, x, y):

        #Параметры по умолчанию
        #Праметры спрайта
        pg.sprite.Sprite.__init__(self)
        self.rect = None
        self.image = None

        #Не боевые статы
        self.level = 1
        self.health = 100
        self.speed = 50

        #боевые статы
        self.damage = 25
        self.critChance = 0.05
        self.critMod = 1.5

    @abstractmethod
    def update(self): #изменения кадра
        pass

    @abstractmethod
    def death(self): #смерть
        pass

    @abstractmethod
    def move(self): #движение юнита в зависимости от вида
        pass

    def getDamage(self): #получение урона

        damage = self.damageMod()
        self.health -= damage

        if self.health <= 0:
            self.death()
        
    # @abstractmethod
    # def getPosition(self):
    #     return (self.x, self.y)

    def damageMod(self): #подсчет урона

        isCritDamage = rd.random() > self.critChance

        if isCritDamage:
            return self.damage * self.critMod
        else:
            return self.damage
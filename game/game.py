# game.py
import pygame as pg

from Poly.code.ground import Ground
from Characters.code.units.hero import Warrior
from Characters.code.units.enemies.walker import Walker
from Characters.code.units.baseUnit import Unit

class Game:

    def __init__(self):
        #Параметры игры
        self.screen = pg.display.set_mode((1200, 800))
        self.clock = pg.time.Clock()
    
        #Объекты
        self.allSprites = pg.sprite.Group()
        self.ground = Ground(self.screen)
        self.hero = Warrior(self.screen.get_size()[0] // 2, self.screen.get_size()[1] // 2, self.screen)
        self.enemy = Walker(0, 0, self.hero, self.screen)
        self.allSprites.add(self.hero)
        self.allSprites.add(self.enemy)

    #Обработка событий
    def handleEvents(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False
        return True
    
    #Изменение кадра
    def update(self, dt):
        self.allSprites.update(dt)
    
    #Прорисовка кадра
    def draw(self):
        self.ground.render()
        self.allSprites.draw(self.screen)
        pg.display.flip()
    
    #Запуск игры
    def run(self):
        running = True
        while running:
            dt = self.clock.tick(60) / 1000.0
            running = self.handleEvents()
            self.update(dt)
            self.draw()
        pg.quit()
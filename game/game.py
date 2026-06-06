# game.py
import pygame as pg

from Poly.code.ground import Ground
from Characters.code.units.hero import Warrior
from Characters.code.units.enemies.walker import Walker
from Characters.code.units.baseUnit import Unit
from Main_menu.windows import ScreenManager

DeepSkyBlue = (0, 191, 255)
Gray = (128, 128, 128)
DimGray = (105, 105, 105)
Gainsboro = (220, 220, 220)
Black = (0, 0, 0)


class Game:

    def __init__(self):
        #Параметры игры
        self.screen = pg.display.set_mode((1200, 800))
        self.clock = pg.time.Clock()

        self.font_title = pg.font.Font(None, 74)
        self.font_button = pg.font.Font(None, 48)
    
        #Объекты
        self.allSprites = pg.sprite.Group()
        self.ground = Ground(self.screen)
        self.hero = Warrior(self.screen.get_size()[0] // 2, self.screen.get_size()[1] // 2, self.screen)
        self.enemy = Walker(0, 0, self.hero, self.screen)
        self.allSprites.add(self.hero)
        self.allSprites.add(self.enemy)
        self.screen_manager = ScreenManager(self.screen, 1200, 800, self.font_title, self.font_button)

        self.current_state = "menu"  
        self.running = True

    #Обработка событий
    def handleEvents(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                return False
            
            # Обработка меню
            if self.current_state == "menu":
                action = self.screen_manager.handle_menu_events(event)
                if action == "quit":
                    self.running = False
                    return False
                elif action == "game":
                    self.current_state = "game"
                elif action == "shop":
                    self.current_state = "shop"
                        
            elif self.current_state == "shop":
                action = self.screen_manager.handle_back_event(event)
                if action == "menu":
                    self.current_state = "menu"

        return True
    
    #Изменение кадра
    def update(self, dt):
        if self.current_state == "game":
            self.allSprites.update(dt)
        
    
    #Прорисовка кадра
    def draw(self):
        if self.current_state == "menu":
            self.screen_manager.draw_menu()
        elif self.current_state == "shop":
            self.screen_manager.draw_shop()
        elif self.current_state == "quit":
            running = False
        elif self.current_state == "game":
            self.ground.render()
            self.allSprites.draw(self.screen)
            pg.display.flip()
            return
        
        pg.display.flip()
    
    #Запуск игры
    def run(self):
        
        while self.running:
            dt = self.clock.tick(60) / 1000.0
            self.handleEvents()
            self.update(dt)
            self.draw()
        pg.quit()


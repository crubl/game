import pygame
from Main_menu.Buttons import Button
from constans import *

class ScreenManager: #класс для отрисовки кнопок

    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.font_title = pygame.font.Font(None, 74)
        self.font_button = pygame.font.Font(None, 48)

        self.menu_buttons = [
        Button(SCREEN_WIDTH//10, 200, 200, 60, "PLAY", DIM_GRAY, GAINSBORO, "game"),

        Button(SCREEN_WIDTH//10, 300, 200, 60, "SHOP", DIM_GRAY, GAINSBORO, "shop"),

        Button(SCREEN_WIDTH//10, 400, 200, 60, "QUIT", DIM_GRAY, GAINSBORO, "quit")
    ]
        self.Back_Key = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 100, 200, 50,
                                "Назад в меню", GRAY, GAINSBORO, "menu")
        
    def draw_menu(self): #отрисовка главного меню

        self.screen.fill(DEEP_SKY_BLUE)

        #отрисовка названия игры
        title = self.font_title.render("МОЯ ИГРА", True, GRAY)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//5, 100))
        self.screen.blit(title, title_rect)

        for button in self.menu_buttons:
            button.draw(self.screen, self.font_button)

    def draw_shop(self):

        self.screen.fill(BLACK)

        self.Back_Key.draw(self.screen, self.font_button)

    def handle_menu_events(self, event):
        #"""Обработка событий для кнопок меню"""
        for button in self.menu_buttons:
            action = button.handle_event(event)
            if action:
                return action
        return None
    
    def handle_back_event(self, event):
        #"""Обработка событий для кнопки назад"""
        return self.Back_Key.handle_event(event)

    
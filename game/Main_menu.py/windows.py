import pygame
from Buttons import Button

WIDTH, HEIGHT = 800,600

DeepSkyBlue = (0, 191, 255)
Gray = (128, 128, 128)
DimGray = (105, 105, 105)
Gainsboro = (220, 220, 220)
Black = (0, 0, 0)

# Шрифты
font_title = pygame.font.Font(None, 74)
font_button = pygame.font.Font(None, 48)

class ScreenManager: #класс для отрисовки кнопок

    def __init__(self, screen, width, height, font_title, font_button):
        self.screen = screen
        self.width = width
        self.height = height
        self.font_title = font_title
        self.font_button = font_button

        self.Menu_Keys = [
        Button(WIDTH//10, 200, 200, 60, "PLAY", DimGray, Gainsboro, "game"),

        Button(WIDTH//10, 300, 200, 60, "SHOP", DimGray, Gainsboro, "shop"),

        Button(WIDTH//10, 400, 200, 60, "QUIT", DimGray, Gainsboro, "quit")
    ]
        self.Back_Key = Button(WIDTH // 2 - 100, HEIGHT - 100, 200, 50,
    "Назад в меню", Gray, Gainsboro, "back")
        
    def draw_menu(self): #отрисовка главного меню

        self.screen.fill(DeepSkyBlue)

        #отрисовка названия игры
        title = font_title.render("МОЯ ИГРА", True, Gray)
        title_rect = title.get_rect(center=(WIDTH//5, 100))
        self.screen.blit(title, title_rect)

        for button in self.Menu_Keys:
            button.draw(self.screen, self.font_button)

    def draw_shop(self):

        self.screen.fill(Black)

        self.Back_Key.draw(self.screen, self.font_button)

    
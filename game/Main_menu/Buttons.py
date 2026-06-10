from constans import *
import pygame

# Шрифты


class Button:
    
    def __init__ (self, x, y, widht, heigt, text, color, hover_color, action = None):
        self.key = pygame.Rect(x, y, widht, heigt)
        self.text = text
        self.color = color
        self.action = action
        self.hover_color = hover_color
        self.is_hovered = False
        self.font_title = pygame.font.Font(None, 74)
        self.font_button = pygame.font.Font(None, 48)

    def draw(self, screen, font):
        #выбор цвета при наведении
        color = self.hover_color if self.is_hovered else self.color

        #Рисуем кнопку
        pygame.draw.rect(screen, color, self.key)

        #текст на кнопке
        text_surface = self.font_button.render(self.text, True, (0,0,0))
        text_rect = text_surface.get_rect(center = self.key.center)
        screen.blit(text_surface, text_rect)

    #обработка действий с кнопками
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.key.collidepoint(event.pos)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.is_hovered:
                if self.action:
                    return self.action
        return None
    
    


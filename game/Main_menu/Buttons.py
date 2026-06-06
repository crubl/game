import pygame

DeepSkyBlue = (0, 191, 255)
Gray = (128, 128, 128)
DimGray = (105, 105, 105)
Gainsboro = (220, 220, 220)
Black = (0, 0, 0)

# Шрифты
font_title = pygame.font.Font(None, 74)
font_button = pygame.font.Font(None, 48)

class Button:
    
    def __init__ (self, x, y, widht, heigt, text, color, hover_color, action = None):
        self.key = pygame.Rect(x, y, widht, heigt)
        self.text = text
        self.color = color
        self.action = action
        self.hover_color = hover_color
        self.is_hovered = False

    def draw(self, screen, font):
        #выбор цвета при наведении
        color = self.hover_color if self.is_hovered else self.color

        #Рисуем кнопку
        pygame.draw.rect(screen, color, self.key)

        #текст на кнопке
        text_surface = font_button.render(self.text, True, (0,0,0))
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
    
    


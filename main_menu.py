import pygame

pygame.init()

#настройки экрана
WIDTH, HEIGHT = 800,600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

#Цвета
DeepSkyBlue = (0, 191, 255)
Gray = (128, 128, 128)
DimGray = (105, 105, 105)
Gainsboro = (220, 220, 220)
Black = (0, 0, 0)

# Шрифты
font_title = pygame.font.Font(None, 74)
font_button = pygame.font.Font(None, 48)

#Класс для создания кнопок
class Button:
    def __init__ (self, x, y, widht, heigt, text, color, hover_color, action = None):
        self.key = pygame.Rect(x, y, widht, heigt)
        self.text = text
        self.color = color
        self.action = action
        self.hover_color = hover_color
        self.is_hovered = False

    def draw(self,screen):
        #выбор цвета при наведении
        color = self.hover_color if self.is_hovered else self.color

        #Рисуем кнопку
        pygame.draw.rect(screen, color, self.key)

        #текст на кнопке
        text_surface = font_button.render(self.text, True, Black)
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
    
    #функция магазина
def shop_loop():
    running = True
    clock = pygame.time.Clock()

    #кнопка назад
    back_key = Button(WIDTH // 2 - 100, HEIGHT - 100, 200, 50,
    "Назад в меню", Gray, Gainsboro, "back")

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

            action = back_key.handle_event(event)
            if action == "back":
                return "menu"

        screen.fill(Black)
        back_key.draw(screen)
        pygame.display.update()
        clock.tick(60)
    return "quit"
    
def main_menu(): #главное меню

    #кнопки
    Keys = [
        Button(WIDTH//10, 200, 200, 60, "PLAY", DimGray, Gainsboro, "game"),

        Button(WIDTH//10, 300, 200, 60, "SHOP", DimGray, Gainsboro, "shop"),

        Button(WIDTH//10, 400, 200, 60, "QUIT", DimGray, Gainsboro, "quit")
    ]    

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

            #проверка нажатия на все кнопки
            for button in Keys:
                action = button.handle_event(event)
                if action:
                    return action
            
        screen.fill(DeepSkyBlue)

        #отрисовка названия игры
        title = font_title.render("МОЯ ИГРА", True, Gray)
        title_rect = title.get_rect(center=(WIDTH//5, 100))
        screen.blit(title, title_rect)

        for button in Keys:
            button.draw(screen)

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    running = True
    current_state = "menu"

    while running:
        if current_state == "menu":
            result = main_menu()
            if result == "game":
                current_state = "game"
            elif result == "shop":
                current_state = "shop"
            elif result == "quit":
                running = False
                
        elif current_state == "game":
            result = shop_loop()
            if result == "menu":
                current_state = "menu"
            elif result == "quit":
                running = False
                
        elif current_state == "shop":
            result = shop_loop()
            if result == "menu":
                current_state = "menu"
            elif result == "quit":
                running = False




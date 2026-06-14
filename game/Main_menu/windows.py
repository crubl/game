import pygame
from Main_menu.Buttons import Button
from Main_menu.shop import Shop
from constans import *

class ScreenManager: #класс для отрисовки кнопок

    def __init__(self, screen, width, height, font_title, font_button, font_small=None, shop=None):
        self.screen = screen
        self.width = width
        self.height = height
        self.shop = shop
        self.font_title = pygame.font.Font(None, 74)
        self.font_button = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)

        self.menu_buttons = [
        Button(SCREEN_WIDTH//10, 200, 200, 60, "PLAY", DIM_GRAY, GAINSBORO, "game"),

        Button(SCREEN_WIDTH//10, 300, 200, 60, "SHOP", DIM_GRAY, GAINSBORO, "shop"),

        Button(SCREEN_WIDTH//10, 400, 200, 60, "QUIT", DIM_GRAY, GAINSBORO, "quit")
    ]
        self.shop_back_button = Button(
            self.width//2 - 100, 
            self.height - 100, 
            200, 50,
            "Назад в меню", GRAY, GAINSBORO, "menu"
        )

        self.shop_upgrade_buttons = []

        if self.shop:
            self.create_shop_buttons(self.shop)

    def set_shop(self, shop):
        """Установить магазин после его создания"""
        self.shop = shop
        self.create_shop_buttons(shop)
    
    def create_shop_buttons(self, shop):
        """Создание кнопок магазина"""
        self.shop = shop
        self.shop_upgrade_buttons = []
        
        button_width = 700
        button_height = 50
        start_x = self.width//2 - button_width//2
        start_y = 180
        spacing = 65
        
        upgrade_colors = {
            'speed': (100, 200, 255),
            'health': (255, 100, 100),
            'damage': (255, 200, 100),
            'crit_damage': (255, 100, 255),
            'crit_chance': (100, 255, 100),
            'exp': (100, 255, 200)
        }
        
        # Получаем список улучшений из shop
        for i, upgrade_name in enumerate(shop.upgrades.keys()):
            y = start_y + i * spacing
            color = upgrade_colors.get(upgrade_name, GAINSBORO)
            
            button = Button(
                start_x, y, button_width, button_height,
                self.get_upgrade_button_text(upgrade_name),
                (50, 50, 50), color,
                f"upgrade_{upgrade_name}"
            )
            self.shop_upgrade_buttons.append(button)
    
    def get_upgrade_button_text(self, upgrade_name):
        """Получить текст для кнопки улучшения"""
        if not self.shop:
            return upgrade_name
        
        level = self.shop.upgrades[upgrade_name]
        price = self.shop.get_price(upgrade_name)
        max_level = self.shop.max_upgrade
        
        upgrade_names_ru = {
            'speed': 'Скорость +20',
            'health': 'Здоровье +75',
            'damage': 'Урон +15',
            'crit_damage': 'Крит урон +0.1x',
            'crit_chance': 'Крит шанс +3%',
            'exp': 'Множитель опыта +0.1x'
        }
        
        text = upgrade_names_ru.get(upgrade_name, upgrade_name)
        
        if level >= max_level:
            return f"{text} (МАКС.)"
        else:
            return f"{text} (ур. {level}/{max_level}) - {price} монет"
        
    def draw_menu(self): #отрисовка главного меню

        self.screen.fill(DEEP_SKY_BLUE)

        #отрисовка названия игры
        title = self.font_title.render("МОЯ ИГРА", True, GRAY)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//5, 100))
        self.screen.blit(title, title_rect)

        for button in self.menu_buttons:
            button.draw(self.screen, self.font_button)

    def draw_shop(self):
        """Отрисовка магазина"""

        if self.shop is None:
            print("Магазин не инициализирован!")
            return

        self.screen.fill(BLACK)
        
        # Заголовок
        title = self.font_title.render("МАГАЗИН", True, GAINSBORO)
        title_rect = title.get_rect(center=(self.width//2, 60))
        self.screen.blit(title, title_rect)
        
        # Отображение монет
        coins_text = self.font_button.render(f"Монеты: {self.shop.coins}", True, GOLD)
        coins_rect = coins_text.get_rect(center=(self.width//2, 120))
        self.screen.blit(coins_text, coins_rect)
        
        # Кнопки улучшений
        for button in self.shop_upgrade_buttons:
            button.draw(self.screen, self.font_button)
        
        # Кнопка назад
        self.shop_back_button.draw(self.screen, self.font_button)
        
        # Отображение информации о герое
        #self.draw_hero_stats()
        
        # Отображение сообщения если есть
        if self.shop.message and self.shop.message_timer > 0:
            msg = self.font_small.render(self.shop.message, True, GOLD)
            msg_rect = msg.get_rect(center=(self.width//2, self.height - 50))
            self.screen.blit(msg, msg_rect)
        
        
    # def draw_hero_stats(self):
    #     """Отрисовка статистики героя"""
    #     if not hasattr(self, 'shop') or not self.shop.hero:
    #         return
        
    #     hero = self.shop.hero
        
    #     # Заголовок статистики
    #     stats_title = self.font_small.render("ХАРАКТЕРИСТИКИ ГЕРОЯ", True, GAINSBORO)
    #     stats_title_rect = stats_title.get_rect(topleft=(50, 180))
    #     self.screen.blit(stats_title, stats_title_rect)
        
    #     # Статы героя
    #     stats = [
    #         (f"Здоровье: {hero.health}/{hero.max_health}", (255, 100, 100)),
    #         (f"Скорость: {hero.speed}", (100, 200, 255)),
    #         (f"Урон: {hero.damage}", (255, 200, 100)),
    #         (f"Крит шанс: {hero.critChance * 100:.1f}%", (100, 255, 100)),
    #         (f"Крит урон: {hero.critMod:.1f}x", (255, 100, 255)),
    #         (f"Множитель опыта: {hero.exp_multiplier:.1f}x", (100, 255, 200)),
    #         (f"Уровень: {hero.level}", (200, 200, 200)),
    #         (f"Опыт: {hero.exp}/{hero.exp_to_next_level}", (200, 200, 100))
    #     ]
        
    #     start_y = 220
    #     for i, (stat_text, color) in enumerate(stats):
    #         stat = self.font_small.render(stat_text, True, color)
    #         stat_rect = stat.get_rect(topleft=(50, start_y + i * 30))
    #         self.screen.blit(stat, stat_rect)
    
    def update_shop_buttons(self):
        """Обновить текст всех кнопок магазина"""
        for button in self.shop_upgrade_buttons:
            upgrade_name = button.action.replace('upgrade_', '')
            button.text = self.get_upgrade_button_text(upgrade_name)
    
    def handle_menu_events(self, event):
        """Обработка событий меню"""
        for button in self.menu_buttons:
            action = button.handle_event(event)
            if action:
                return action
        return None
    
    def handle_shop_events(self, event):
        """Обработка событий магазина"""
        if not self.shop:
            print("Ошибка: shop = None!")
            return None, None
        
        if not self.shop_upgrade_buttons:
            print("Ошибка: shop_upgrade_buttons пуст!")
            return None, None
        
        
        # Обработка кнопок улучшений
        for button in self.shop_upgrade_buttons:
            action = button.handle_event(event)
            if action and action.startswith('upgrade_'):
                upgrade_name = action.replace('upgrade_', '')
                success, message = self.shop.upgrade(upgrade_name)
                if success:
                    self.update_shop_buttons()
                return success, message
        
        # Обработка кнопки назад
        action = self.shop_back_button.handle_event(event)
        if action == "menu":
            return True, "menu"
        
        return None, None


    
    # def handle_back_event(self, event):
    #     #"""Обработка событий для кнопки назад"""
    #     return self.Back_Key.handle_event(event)

    
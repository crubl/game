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

        self.menu_button_images = self.load_menu_button_images()

        self.menu_buttons = []
        menu_actions = [
            ("PLAY", "game", self.menu_button_images[0]),
            ("SHOP", "shop", self.menu_button_images[1]),
            ("QUIT", "quit", self.menu_button_images[2])
        ]

        button_spacing = 20
        button_positions = []
        for text, action, image in menu_actions:
            button_text = "" if image is not None else text
            button_image = None
            width = 200
            height = 60

            if image is not None:
                img_width, img_height = image.get_size()
                max_width = 260
                if img_width > max_width:
                    scale = max_width / img_width
                    width = max_width
                    height = max(60, int(img_height * scale))
                    button_image = pygame.transform.smoothscale(image, (width, height))
                else:
                    width = img_width
                    height = img_height
                    button_image = image

            button_positions.append((button_text, action, button_image, width, height))

        total_height = sum(height for _, _, _, width, height in button_positions) + button_spacing * (len(button_positions) - 1)
        start_y = self.height // 2 - total_height // 2
        x = SCREEN_WIDTH // 10

        for text, action, button_image, width, height in button_positions:
            self.menu_buttons.append(Button(x, start_y, width, height, text, DIM_GRAY, GAINSBORO, action, image=button_image))
            start_y += height + button_spacing

        self.menu_background = self.load_menu_background()
        self.shop_background = self.load_shop_background()
        self.shop_button_bg = self.load_shop_button_background()

        # Separate back-button background configuration
        back_width = 250
        back_height = 50
        self.shop_back_button_bg = None
        if self.shop_button_bg is not None:
            self.shop_back_button_bg = self.scale_image_to_box(self.shop_button_bg, back_width, back_height)

        self.shop_back_button = Button(
            self.width//2 - back_width//2,
            self.height - 100,
            back_width, back_height,
            "Назад в меню", GRAY, GAINSBORO, "menu", image=self.shop_back_button_bg
        )

        self.shop_upgrade_buttons = []

        if self.shop:
            self.create_shop_buttons(self.shop)

    def set_shop(self, shop):
        """Установить магазин после его создания"""
        self.shop = shop
        self.create_shop_buttons(shop)
    
    def scale_image_to_box(self, image, width, height):
        """Масштабировать изображение кнопки без обрезания"""
        if image is None:
            return None

        image = image.convert_alpha()
        img_width, img_height = image.get_size()
        if img_width <= 0 or img_height <= 0:
            return None

        return pygame.transform.smoothscale(image, (width, height))

    def create_shop_buttons(self, shop):
        """Создание кнопок магазина"""
        self.shop = shop
        self.shop_upgrade_buttons = []

        upgrade_names = list(shop.upgrades.keys())
        button_texts = [self.get_upgrade_button_text(name) for name in upgrade_names]
        text_surfaces = [self.font_button.render(text, True, (0, 0, 0)) for text in button_texts]

        min_width = 280
        max_width = 650
        padding_x = 24
        padding_y = 16
        spacing = 2

        max_text_width = max(surf.get_width() for surf in text_surfaces)
        button_width = min(max_width, max(min_width, max_text_width + padding_x * 2))

        max_text_height = max(surf.get_height() for surf in text_surfaces)
        computed = max_text_height * 6 + padding_y * 2
        button_height = max(20, min(280, computed // 3))

        button_sizes = [(button_width, button_height) for _ in text_surfaces]

        total_height = len(button_sizes) * button_height + spacing * (len(button_sizes) - 1)
        start_y = self.height // 2 - total_height // 2
        start_x = self.width - button_width - 50

        upgrade_colors = {
            'speed': (100, 200, 255),
            'health': (255, 100, 100),
            'damage': (255, 200, 100),
            'crit_damage': (255, 100, 255),
            'crit_chance': (100, 255, 100),
            'exp': (100, 255, 200)
        }

        for i, upgrade_name in enumerate(upgrade_names):
            button_width, button_height = button_sizes[i]
            y = start_y + sum(button_sizes[j][1] + spacing for j in range(i))
            color = upgrade_colors.get(upgrade_name, GAINSBORO)

            button_image = None
            if self.shop_button_bg is not None:
                button_image = self.scale_image_to_box(self.shop_button_bg, button_width, button_height)

            button = Button(
                start_x, y, button_width, button_height,
                button_texts[i],
                (50, 50, 50), color,
                f"upgrade_{upgrade_name}",
                image=button_image
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

        if self.menu_background:
            bg = pygame.transform.scale(self.menu_background, (self.width, self.height))
            self.screen.blit(bg, (0, 0))
        else:
            self.screen.fill(DEEP_SKY_BLUE)

        #отрисовка названия игры
        title = self.font_title.render("ROGUE SURVIVORS", True, GRAY)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//4, 100))
        self.screen.blit(title, title_rect)

        for button in self.menu_buttons:
            button.draw(self.screen, self.font_button)

    def draw_shop(self):
        """Отрисовка магазина"""

        if self.shop is None:
            print("Магазин не инициализирован!")
            return

        if self.shop_background:
            bg = pygame.transform.scale(self.shop_background, (self.width, self.height))
            self.screen.blit(bg, (0, 0))
        else:
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
        
        # Отображение сообщения если есть
        if self.shop.message and self.shop.message_timer > 0:
            msg = self.font_small.render(self.shop.message, True, GOLD)
            msg_rect = msg.get_rect(center=(self.width//2, self.height - 50))
            self.screen.blit(msg, msg_rect)
        
        
   
    
    def load_menu_button_images(self):
        """Загрузить спрайт-кнопки для главного меню"""
        try:
            sheet = pygame.image.load(MENU_BUTTONS_SPRITE_PATH).convert_alpha()
            width, height = sheet.get_size()

            cols = [any(sheet.get_at((x, y))[3] > 0 for y in range(height)) for x in range(width)]
            rows = [any(sheet.get_at((x, y))[3] > 0 for x in range(width)) for y in range(height)]

            col_runs = []
            start = None
            for x, filled in enumerate(cols):
                if filled and start is None:
                    start = x
                elif not filled and start is not None:
                    col_runs.append((start, x - 1))
                    start = None
            if start is not None:
                col_runs.append((start, width - 1))

            row_runs = []
            start = None
            for y, filled in enumerate(rows):
                if filled and start is None:
                    start = y
                elif not filled and start is not None:
                    row_runs.append((start, y - 1))
                    start = None
            if start is not None:
                row_runs.append((start, height - 1))

            if len(col_runs) == 3 and row_runs:
                y0, y1 = row_runs[0]
                images = []
                for x0, x1 in col_runs:
                    crop = sheet.subsurface((x0, y0, x1 - x0 + 1, y1 - y0 + 1)).copy()
                    images.append(crop)
                return images

            button_width = max(1, width // 3)
            return [sheet.subsurface((i * button_width, 0, button_width, height)).copy() for i in range(3)]
        except Exception:
            return [None, None, None]

    def load_menu_background(self):
        """Загрузить фон для главного меню"""
        try:
            return pygame.image.load(MENU_BACKGROUND_PATH).convert()
        except Exception:
            return None

    def load_shop_background(self):
        """Загрузить фон для магазина"""
        try:
            return pygame.image.load(SHOP_BACKGROUND_PATH).convert()
        except Exception:
            return None

    def load_shop_button_background(self):
        """Загрузить фон кнопок магазина"""
        try:
            return pygame.image.load(SHOP_BUTTON_BACKGROUND_PATH).convert_alpha()
        except Exception:
            return None

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


    
    

    
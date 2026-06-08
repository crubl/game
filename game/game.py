import pygame as pg

# Проверяем, инициализированы ли шрифты
if not pg.font.get_init():
    pg.font.init()

# Остальные импорты
import os
from Poly.code.game_field import GameField
from Characters.code.units.hero import Warrior
from Characters.code.units.enemies.walker import Walker
from Main_menu.windows import ScreenManager

# Меняем рабочую директорию
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# ==================== НАСТРОЙКИ ====================
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
GAME_TITLE = "Vampire Survivors"
from Characters.code.units.baseUnit import Unit
from Main_menu.windows import ScreenManager

DeepSkyBlue = (0, 191, 255)
Gray = (128, 128, 128)
DimGray = (105, 105, 105)
Gainsboro = (220, 220, 220)
Black = (0, 0, 0)

#font_title = pg.font.Font(None, 74)
#font_button = pg.font.Font(None, 48)


class Game:
    """Основной класс игры с меню и самой игрой"""

    def __init__(self):
        # ==================== ПАРАМЕТРЫ ИГРЫ ====================
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pg.time.Clock()
        self.running = True
        self.current_state = "menu"  # menu, game, shop

        # ==================== ШРИФТЫ ДЛЯ МЕНЮ ====================
        self.font_title = pg.font.Font(None, 74)
        self.font_button = pg.font.Font(None, 48)

        # ==================== МЕНЮ ====================
        self.screen_manager = ScreenManager(
            self.screen, SCREEN_WIDTH, SCREEN_HEIGHT,
            self.font_title, self.font_button
        )

        # ==================== ИГРОВЫЕ ОБЪЕКТЫ ====================
        self.game_field = None   # будет создан при запуске игры
        self.hero = None

    def start_game(self):
        """Запускает новую игру (создаёт поле и игрока)"""
        # Создаём игровое поле
        self.game_field = GameField(self.screen)
        
        # Создаём игрока в центре мира
        self.hero = Warrior(
            self.game_field.world_width // 2,
            self.game_field.world_height // 2,
            self.screen,
            self.game_field
        )
        
        # Передаём игрока в поле
        self.game_field.set_player(self.hero)

    def stop_game(self):
        """Останавливает игру (очищает поле)"""
        self.game_field = None
        self.hero = None

    def handle_events(self):
        """Обработка событий (меню и игра)"""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                return

            # ==================== ОБРАБОТКА МЕНЮ ====================
            if self.current_state == "menu":
                action = self.screen_manager.handle_menu_events(event)
                if action == "quit":
                    self.running = False
                elif action == "game":
                    self.current_state = "game"
                    self.start_game()  # создаём игровое поле
                elif action == "shop":
                    self.current_state = "shop"

            # ==================== ОБРАБОТКА МАГАЗИНА ====================
            elif self.current_state == "shop":
                action = self.screen_manager.handle_back_event(event)
                if action == "menu":
                    self.current_state = "menu"

            # ==================== ОБРАБОТКА ИГРЫ ====================
            elif self.current_state == "game":
                # Проверяем, не закрыли ли игру
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.current_state = "menu"
                        self.stop_game()  # очищаем поле

                # Передаём события в игру (если нужно)
                if self.game_field:
                    self.game_field.handle_events()

    def update(self, dt):
        """Обновление состояния в зависимости от текущего экрана"""
        if self.current_state == "game" and self.game_field:
            self.game_field.update(dt)

    def draw(self):
        """Отрисовка в зависимости от текущего экрана"""
        if self.current_state == "menu":
            self.screen_manager.draw_menu()
        elif self.current_state == "shop":
            self.screen_manager.draw_shop()
        elif self.current_state == "game" and self.game_field:
            self.game_field.draw()
        
        pg.display.flip()

    def run(self):
        """Главный игровой цикл"""
        dt = 0.0
        while self.running:
            self.handle_events()
            self.update(dt)
            self.draw()
            dt = self.clock.tick(60) / 1000.0
        pg.quit()

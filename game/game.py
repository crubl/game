from Characters.code.units.enemies.walker import Walker
from Characters.code.units.baseUnit import Unit
from Characters.code.units.hero import Warrior
from Main_menu.windows import ScreenManager
from Poly.code.game_field import GameField
from Main_menu.shop import Shop
from constans import *
import pygame as pg
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
pg.font.init()


class Game:
    def __init__(self):
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pg.time.Clock()
        self.running = True
        self.current_state = "menu"      # menu, game, shop, game_over

        # ==================== МУЗЫКА ====================
        self.music_on = True
        self.init_audio()
        self.load_menu_music()
        self.start_menu_music()

        # Шрифты
        self.font_title = pg.font.Font(None, 74)
        self.font_button = pg.font.Font(None, 48)
        self.font_small = pg.font.Font(None, 36)

        # Игровые объекты
        self.game_field = None
        self.hero = None
        self.shop = Shop()

        self.screen_manager = ScreenManager(
            self.screen,
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            self.font_title,
            self.font_button,
            self.font_small,
            self.shop
        )

        self.paused = False          # флаг паузы

    def init_audio(self):
        """Инициализация аудио"""
        try:
            pg.mixer.init()
            print("Аудио инициализировано")
        except Exception as e:
            print(f"Ошибка инициализации аудио: {e}")
            self.music_on = False

    def load_menu_music(self):
        """Загрузка музыки для меню"""
        try:
            
            base_dir = os.path.dirname(os.path.abspath(__file__))
            music_path = os.path.join(base_dir, 'sounds', 'menu_music.mp3')
            
            print(f"Ищем музыку: {music_path}")
            
            if os.path.exists(music_path):
                self.menu_music_path = music_path
                print(f"✅ Музыка найдена!")
                self.music_on = True
            else:
                self.menu_music_path = None
                print(f"❌ Файл не найден: {music_path}")
                print(f"Проверьте путь: {base_dir}/sounds/menu_music.mp3")
                self.music_on = False
        except Exception as e:
            print(f"Ошибка загрузки музыки: {e}")
            self.music_on = False

    def start_menu_music(self):
        """Запуск музыки для меню"""
        if not self.music_on or not self.menu_music_path:
            return
        try:
            pg.mixer.music.load(self.menu_music_path)
            pg.mixer.music.set_volume(0.3)  # Громкость 30%
            pg.mixer.music.play(-1)  # Бесконечное повторение
            print("Музыка меню запущена")
        except Exception as e:
            print(f"Не удалось запустить музыку: {e}")
            self.music_on = False

    def toggle_music(self):
        """Включить/выключить музыку"""
        self.music_on = not self.music_on
        if self.music_on:
            self.start_menu_music()
            print("Музыка включена")
        else:
            pg.mixer.music.stop()
            print("Музыка выключена") 

    def start_game(self):
        self.game_field = GameField(self.screen)
        self.hero = Warrior(
            self.game_field.world_width // 2,
            self.game_field.world_height // 2,
            self.screen,
            self.game_field
        )
        self.game_field.set_player(self.hero)
        self.game_field.creatMap(self.hero)
        self.shop.set_hero(self.hero)

        self.screen_manager.set_shop(self.shop)
        self.screen_manager.create_shop_buttons(self.shop)
        self.paused = False

    def stop_game(self):
        self.game_field = None
        self.hero = None
        self.paused = False

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                return

            # ----- МЕНЮ -----
            if self.current_state == "menu":
                action = self.screen_manager.handle_menu_events(event)
                if action == "quit":
                    self.running = False
                elif action == "game":
                    self.current_state = "game"
                    self.start_game()
                    pg.mixer.music.stop()
                elif action == "shop":
                    if self.shop is None:
                        print("Сначала начните игру (нажмите PLAY)!")
                    else:
                        self.current_state = "shop"
                        pg.mixer.music.stop()

                if event.type == pg.KEYDOWN and event.key == pg.K_m:
                    self.toggle_music()        

            # ----- МАГАЗИН -----
            elif self.current_state == "shop":
                action = self.screen_manager.shop_back_button.handle_event(event)
                self.screen_manager.handle_shop_events(event)
                if action == "menu":
                    self.current_state = "menu"
                    self.start_menu_music()

            # ----- ИГРА -----
            elif self.current_state == "game":
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.current_state = "menu"
                        self.stop_game()
                        self.start_menu_music()
                        self.stop_game()
                    elif event.key == pg.K_p:          # <-- ПАУЗА по клавише P
                        self.paused = not self.paused
                    elif event.key == pg.K_F5:
                        if self.shop is not None:
                            self.shop.reset()
                            self.shop.save()
                            if self.hero is not None:
                                self.shop.apply_upgrades_to_hero(self.hero)

                if self.game_field:
                    self.game_field.handle_events()

            # ----- GAME OVER -----
            elif self.current_state == "game_over":
                if event.type == pg.KEYDOWN:
                    self.current_state = "menu"
                    self.stop_game()

    def update(self, dt):
        # Обновляем игру только если мы в игре и не на паузе
        if self.current_state == "game" and self.game_field and not self.paused:
            self.game_field.update(dt)
            # Проверка смерти героя
            if self.hero and self.hero.health <= 0:
                self.current_state = "game_over"

    def draw(self):
        # ОЧИЩАЕМ ЭКРАН – убираем мерцание
        self.screen.fill((0, 0, 0))

        if self.current_state == "menu":
            self.screen_manager.draw_menu()
        elif self.current_state == "shop":
            self.screen_manager.draw_shop()
        elif self.current_state == "game":
            if self.game_field:
                self.game_field.draw()

            # Если пауза – рисуем затемнение и надпись
            if self.paused:
                overlay = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pg.SRCALPHA)
                overlay.fill((0, 0, 0, 128))
                self.screen.blit(overlay, (0, 0))
                pause_text = self.font_title.render("PAUSE", True, (255, 255, 255))
                text_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                self.screen.blit(pause_text, text_rect)

        elif self.current_state == "game_over":
            # Рисуем замороженное поле
            if self.game_field:
                self.game_field.draw()
            # Затемнение и текст
            overlay = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pg.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.screen.blit(overlay, (0, 0))
            game_over_text = self.font_title.render("GAME OVER", True, (255, 50, 50))
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            self.screen.blit(game_over_text, text_rect)
            hint_text = self.font_small.render("Press any key to return to menu", True, (255, 255, 255))
            hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
            self.screen.blit(hint_text, hint_rect)

        pg.display.flip()

    def run(self):
        dt = 0.0
        while self.running:
            self.handle_events()
            self.update(dt)
            self.draw()
            dt = self.clock.tick(60) / 1000.0
        pg.quit()
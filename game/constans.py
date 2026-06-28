# ================= Экран =============================
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
GAME_TITLE = "Vampire Survivors"
# =====================================================

# ================== Цвета ============================
DEEP_SKY_BLUE = (0, 191, 255)
GRAY = (128, 128, 128)
DIM_GRAY = (105, 105, 105)
GAINSBORO = (220, 220, 220)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)
# =====================================================

# ==================== Герой ==========================
#Параметры спрайта
SPRITE_PATH_HERO = "./Characters/sprites/hero/hero.png"
# =====================================================

# ==================== Враг ===========================
#Параметры спрайта
SPRITE_PATH_ENEMY = "./Characters/sprites/enemies/enemy.png"
# =====================================================

# ==================== Меню ============================
MENU_BACKGROUND_PATH = "./Main_menu/sprites/menu_background.png"
MENU_BUTTONS_SPRITE_PATH = "./Main_menu/sprites/menu_buttons.png"
SHOP_BACKGROUND_PATH = "./Main_menu/sprites/shop_background.png"
SHOP_BUTTON_BACKGROUND_PATH = "./Main_menu/sprites/shop_button_bg.png"
# =====================================================

# ==================== Поле ===========================
#Размеры
WORLD_WIDTH = 2400
WORLD_HEIGHT = 1800

#Параметры спрайта
GROUND_SPRITE_PATH = "./Poly/sprites/ground.webp"

# ==================== Спавн врагов ===================
SPAWN_DELAY = 1.0
MAX_ENEMIES = 1000

# ==================== Ивенты ====================
RING_EVENTS = [
    {"time": 15.0, "count": 12, "radius": 300, "speed_multiplier":0.5}, #time - через какое время, count - количество врагов, radius - радиус кольца
]
import json
import os

DeepSkyBlue = (0, 191, 255)
Gray = (128, 128, 128)
DimGray = (105, 105, 105)
Gainsboro = (220, 220, 220)
Black = (0, 0, 0)

# Шрифты
#font_title = pygame.font.Font(None, 74)
#font_button = pygame.font.Font(None, 48)

PlayerSpeed = 300          # скорость передвижения (пикселей/сек)
PlayerHeath = 750         # макс хп
PlayerDamage = 150         # урон
PlayerCrit = 1.1           # крит урон
PlayerCritChange = 0      # крит шанс

from Main_menu.Buttons import Button

class Shop:

    def __init__(self, save_path=None):
        self.save_path = save_path or os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', 'save.json')
        )
        self.upgrades_info = {
            'speed': {'name': 'Скорость', 'base_price': 100, 'increase': 20},
            'health': {'name': 'Здоровье', 'base_price': 100, 'increase': 75},
            'damage': {'name': 'Урон', 'base_price': 150, 'increase': 15},
            'crit_damage': {'name': 'Крит урон', 'base_price': 200, 'increase': 0.1},
            'crit_chance': {'name': 'Крит шанс', 'base_price': 250, 'increase': 0.03}
        }

        self.upgrades = {
            'speed': 0,
            'health': 0,
            'damage': 0,
            'crit_damage': 0,
            'crit_chance': 0
        }
        
        self.max_upgrade = 10

        self.coins = 10000

        self.message = ""
        self.message_timer = 0
        self.hero = None
        self.load()

    def get_price(self, upgrade_name):
        """Получить цену улучшения с учётом уровня прокачки"""
        base_price = self.upgrades_info[upgrade_name]['base_price']
        level = self.upgrades[upgrade_name]
        # Цена увеличивается на 15% за каждый уровень
        return int(base_price * (1 + level * 0.15))
        
    def upgrade(self, upgrade_name):
        """Применить улучшение"""
        if upgrade_name not in self.upgrades:
            return False, "Неизвестное улучшение!"
    
        if self.upgrades[upgrade_name] >= self.max_upgrade:
            return False, "Максимальный уровень достигнут!"
    
        price = self.get_price(upgrade_name)
        if self.coins < price:
            return False, f"Не хватает монет! Нужно {price}"
        
            # Снимаем монеты
        self.coins -= price
        
        # Увеличиваем уровень улучшения
        self.upgrades[upgrade_name] += 1
        
        # Применяем улучшение к герою
        increase = self.upgrades_info[upgrade_name]['increase']
        
        #if upgrade_name == 'speed':
        #    self.hero.speed += increase
        #elif upgrade_name == 'health':
        #    self.hero.max_health += increase
        #    self.hero.health = self.hero.max_health
        #elif upgrade_name == 'damage':
        #    self.hero.damage += increase
        #elif upgrade_name == 'crit_damage':
        #    self.hero.critMod += increase
        #elif upgrade_name == 'crit_chance':
        #    self.hero.critChance += increase
        #elif upgrade_name == 'exp':
         #   self.hero.exp_multiplier += increase
        
        # Устанавливаем сообщение
        #self.message = f"Улучшение {self.upgrades_info[upgrade_name]['name']} успешно!"
        self.message = f"Улучшение {self.upgrades_info[upgrade_name]['name']} куплено! (Уровень {self.upgrades[upgrade_name]}/{self.max_upgrade})"
        self.message_timer = 120

        if self.hero is not None:
            self.apply_upgrades_to_hero(self.hero)

        self.save()
        return True, self.message

    def set_hero(self, hero):
        """Установить текущего героя для немедленного применения улучшений"""
        self.hero = hero
        if self.hero is not None:
            self.apply_upgrades_to_hero(self.hero)

    def apply_upgrades_to_hero(self, hero):
        """Применить сохранённые уровни улучшений к герою"""
        hero.speed = 300 + self.upgrades['speed'] * self.upgrades_info['speed']['increase']
        old_max = hero.maxHealth
        hero.maxHealth = 750 + self.upgrades['health'] * self.upgrades_info['health']['increase']
        if hero.health >= old_max:
            hero.health = hero.maxHealth
        else:
            hero.health = min(hero.health, hero.maxHealth)

        weapon = getattr(hero, 'weapon', None)
        if weapon is not None:
            weapon.damage = 150 + self.upgrades['damage'] * self.upgrades_info['damage']['increase']
            weapon.critChance = min(1.0, 0.1 + self.upgrades['crit_chance'] * self.upgrades_info['crit_chance']['increase'])
            weapon.critMultiplier = 1.8 + self.upgrades['crit_damage'] * self.upgrades_info['crit_damage']['increase']

    def save(self):
        """Сохранить состояние магазина и покупок в файл"""
        try:
            data = {
                'coins': self.coins,
                'upgrades': self.upgrades
            }
            save_dir = os.path.dirname(self.save_path)
            if save_dir and not os.path.exists(save_dir):
                os.makedirs(save_dir, exist_ok=True)
            with open(self.save_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения магазина: {e}")

    def load(self):
        """Загрузить состояние магазина из файла, если файл существует"""
        if not os.path.exists(self.save_path):
            return
        try:
            with open(self.save_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.coins = data.get('coins', self.coins)
            saved_upgrades = data.get('upgrades', {})
            for key in self.upgrades:
                self.upgrades[key] = saved_upgrades.get(key, self.upgrades[key])
        except Exception as e:
            print(f"Ошибка загрузки магазина: {e}")

    def update_message_timer(self):
        """Обновление таймера сообщения"""
        if self.message_timer > 0:
            self.message_timer -= 1
            if self.message_timer == 0:
                self.message = ""

    def reset(self):
        """Сброс улучшений (для новой игры)"""
        self.upgrades = {key: 0 for key in self.upgrades}
        self.coins = 10000
        self.message = ""
        self.message_timer = 0
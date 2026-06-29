import pygame as pg
import random
import math
from constans import *
from .camera import Camera
from Characters.code.units.enemies.walker import Walker
from .polyMap import Map
from Events.EventManager import EventManager
from Events.RingSpawnEvent import RingSpawnEvent
from constans import RING_EVENTS


class GameField:
    """Игровое поле — управляет камерой, игроком, врагами и спавном"""
    
    def __init__(self, screen, shop = None):
        self.screen = screen
        self.shop = shop
        self.clock = pg.time.Clock()
        self.running = True
        
        # Размеры мира
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.world_width = WORLD_WIDTH
        self.world_height = WORLD_HEIGHT
        
        # ==================== Загрузка земли ====================
        self.ground_sprite = None
        self.tile_width = 0
        self.tile_height = 0
        self.load_ground_sprite()
        self.map = None
        
        # Камера
        self.camera = Camera(
            self.screen_width, self.screen_height,
            self.world_width, self.world_height
        )
        
        # Игрок и враги
        self.player = None
        self.enemies = []
        
        # Настройки спавна
        self.spawn_timer = 0
        self.spawn_delay = SPAWN_DELAY
        self.max_enemies = MAX_ENEMIES

        # ==================== Ивенты ====================
        self.event_manager = EventManager()
        self._setup_events()
        
    def _setup_events(self):
        """Настраивает ивенты из конфига"""
        for event_config in RING_EVENTS:
            ring_event = RingSpawnEvent(
                trigger_time=event_config["time"],
                enemy_count=event_config["count"],
                radius=event_config["radius"],
                enemy_class=Walker,
                speed_multiplier=event_config.get("speed_multiplier", 1.0)
            )
            self.event_manager.add_event(ring_event)
        
    def load_ground_sprite(self):
        """Загружает спрайт земли"""
        self.ground_sprite = pg.image.load(GROUND_SPRITE_PATH).convert_alpha()
        self.tile_width = self.ground_sprite.get_width()
        self.tile_height = self.ground_sprite.get_height()
        print(f"Земля загружена: {GROUND_SPRITE_PATH} ({self.tile_width}x{self.tile_height})")

    def creatMap(self, hero):
        self.map = Map(math.ceil(hero.radius * 2.2))
    
    def draw_ground(self):
        """Рисует землю с учётом камеры"""
        # Вычисляем видимую область мира
        start_x = int(self.camera.x // self.tile_width) * self.tile_width
        start_y = int(self.camera.y // self.tile_height) * self.tile_height
        end_x = self.camera.x + self.screen_width
        end_y = self.camera.y + self.screen_height
        
        # Отрисовываем только видимые тайлы
        x = start_x
        while x < end_x:
            y = start_y
            while y < end_y:
                # Преобразуем мировые координаты в экранные
                screen_x = x - self.camera.x
                screen_y = y - self.camera.y
                self.screen.blit(self.ground_sprite, (screen_x, screen_y))
                y += self.tile_height
            x += self.tile_width
    
    def set_player(self, player):
        """Устанавливает игрока, за которым следит камера"""
        self.player = player
    
    def clampInterval(self, center, minVal, maxVal, offset=300):
            low = int(max(minVal, center - offset))
            high = int(min(maxVal, center + offset))
            if low > high:
                low = high = int(center)
            return low, high
    
    def spawn_enemy(self):
        """Создаёт врага за пределами экрана"""
        if len(self.enemies) >= self.max_enemies:
            return

        side = random.randint(0, 3)
        
        if side == 0: # сверху
            xMin, xMax = self.clampInterval(self.player.x, 0, self.world_width)
            x = random.randint(xMin, xMax)
            y = -50
        elif side == 1:# снизу
            xMin, xMax = self.clampInterval(self.player.x, 0, self.world_width)
            x = random.randint(xMin, xMax)
            y = self.world_height + 50
        elif side == 2:# слева
            x = -50
            yMin, yMax = self.clampInterval(self.player.y, 0, self.world_height)
            y = random.randint(yMin, yMax)
        else:# справа
            x = self.world_width + 50
            yMin, yMax = self.clampInterval(self.player.y, 0, self.world_height)
            y = random.randint(yMin, yMax)
        
        enemy = Walker(x, y, self.player, self.screen)
        self.enemies.append(enemy)

        

    def drawHealthbars(self):
        """Рисует полоски здоровья поверх всех спрайтов"""
        # Полоски здоровья врагов
        for enemy in self.enemies:
            if enemy.health <= 0:
                continue
            screen_pos = self.camera.apply(enemy.x, enemy.y)
            bar_width = 30
            bar_height = 4
            health_percent = enemy.health / enemy.maxHealth
            bar_x = screen_pos[0] - bar_width // 2
            bar_y = screen_pos[1] - enemy.image.get_height() // 2 - 6
            pg.draw.rect(self.screen, (60, 60, 60), (bar_x, bar_y, bar_width, bar_height))
            pg.draw.rect(self.screen, (255, 0, 0), (bar_x, bar_y, bar_width * health_percent, bar_height))

    def resolveСollision(self, a, b):
        """Раздвигает два круглых объекта"""
        dx = a.x - b.x
        dy = a.y - b.y
        dist = math.hypot(dx, dy)
        minDist = a.radius + b.radius
        if dist < minDist and dist > 0:
            overlap = minDist - dist
            angle = math.atan2(dy, dx)
            pushX = math.cos(angle) * overlap * 0.5
            pushY = math.sin(angle) * overlap * 0.5
            a.x += pushX
            a.y += pushY
            b.x -= pushX
            b.y -= pushY

            # Обновляем rectы
            if hasattr(a, 'rect'):
                a.rect.center = (a.x, a.y)
            if hasattr(b, 'rect'):
                b.rect.center = (b.x, b.y)
    
    def update(self, dt):
        """Обновляет состояние всех объектов"""
        if self.player:
            self.player.update(dt)
            self.camera.update(self.player.x, self.player.y)

            self.event_manager.update(dt, self)  #Ивенты
            
            self.spawn_timer += dt
            if self.spawn_timer >= self.spawn_delay:
                self.spawn_timer = 0
                self.spawn_enemy()
            
            for enemy in self.enemies[:]:
                enemy.update(dt)
                if enemy.health <= 0:
                    self.shop.add_coins(10)
                    self.enemies.remove(enemy)
            
            if hasattr(self.player, 'weapon') and self.player.weapon:
                for effect, hitbox in self.player.weapon.getActiveHitboxes():
                    for enemy in self.enemies:
                        if enemy.health <= 0:
                            continue
                        if hitbox.colliderect(enemy.rect):
                            # Проверяем, можно ли нанести урон (например, один раз за эффект)
                            if hasattr(effect, 'onHitEnemy'):
                                if not effect.onHitEnemy(enemy):
                                    continue
                            # Рассчитываем урон (можно взять из оружия + крит)
                            damage = self.player.weapon.damage
                            # Добавим случайный крит (если есть параметры)
                            if hasattr(self.player.weapon, 'critChance') and hasattr(self.player.weapon, 'critMultiplier'):
                                import random
                                if random.random() < self.player.weapon.critChance:
                                    damage = int(damage * self.player.weapon.critMultiplier)
                            enemy.getDamage(damage)

            #Очищаем и перестраиваем сетку
            self.map.clear()
            self.map.add(self.player)
            for enemy in self.enemies:
                if enemy.health > 0:
                    self.map.add(enemy)
            
            nearby = self.map.getNearby(self.player)
            collidingPairs = []
            for unit in nearby:
                if unit is self.player:
                    continue
                if unit.collidesWith(self.player):
                    collidingPairs.append((self.player, unit))
            
            for player, enemy in collidingPairs:
                # enemy.getDamage()
                player.getDamage(enemy.damage)
            
            for a, b in collidingPairs:
                self.resolveСollision(a, b)
            
            #Отталкивание врагов между собой 
            processed = set()
            for enemy in self.enemies:
                if enemy.health <= 0:
                    continue
                neighbors = self.map.getNearby(enemy)
                for other in neighbors:
                    if other is enemy or not isinstance(other, Walker):
                        continue
                    pair = (id(enemy), id(other))
                    if pair in processed:
                        continue
                    processed.add(pair)
                    if enemy.collidesWith(other):
                        self.resolveСollision(enemy, other)
    
    def draw(self):
        """Отрисовывает всё игровое поле"""
        # Рисуем землю (фон)
        self.draw_ground()
        
        # Враги (только видимые камерой)
        for enemy in self.enemies:
            if self.camera.is_visible(enemy.x, enemy.y):
                enemy.draw(self.screen, self.camera)
        # Игрок
        if self.player:
            self.player.draw(self.screen, self.camera)
            if hasattr(self.player, 'weapon'):
                self.player.weapon.draw(self.screen, self.camera)
        self.drawHealthbars() 
    
    def handle_events(self):
        """Обработка событий (клавиши, закрытие окна)"""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.running = False
                elif event.key == pg.K_F1:
                    self.show_debug = not self.show_debug
                elif event.key == pg.K_F2:
                    self.show_grid = not self.show_grid

    def set_shop(self, shop):
        """Установить магазин"""
        self.shop = shop
        print(f"Shop установлен в GameField")
    
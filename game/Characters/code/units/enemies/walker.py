from Characters.code.units.baseUnit import Unit
from constans import *
import pygame as pg
import math

class Walker(Unit):
    
    def __init__(self, x, y, hero, screen):
        super().__init__(x, y)
        self.hero = hero
        self.screen = screen

        # ===== НАСТРОЙКА РАЗМЕРА =====
        self.scale_factor = 1.0   # 1.0 = исходный размер, можно поставить 1.2 для небольшого увеличения

        self.sprite_sheet = pg.image.load(SPRITE_PATH_ENEMY).convert_alpha()
        orig_w = self.sprite_sheet.get_width() // 8
        orig_h = self.sprite_sheet.get_height() // 2
        new_w = int(orig_w * self.scale_factor)
        new_h = int(orig_h * self.scale_factor)

        # Кадры и маски (как раньше)
        self.frames_idle = []
        self.masks_idle = []
        for col in range(8):
            frame = self.sprite_sheet.subsurface((col * orig_w, 0, orig_w, orig_h))
            scaled_frame = pg.transform.smoothscale(frame, (new_w, new_h))
            self.frames_idle.append(scaled_frame)
            self.masks_idle.append(pg.mask.from_surface(scaled_frame))

        self.frames_walk = []
        self.masks_walk = []
        for col in range(8):
            frame = self.sprite_sheet.subsurface((col * orig_w, orig_h, orig_w, orig_h))
            scaled_frame = pg.transform.smoothscale(frame, (new_w, new_h))
            self.frames_walk.append(scaled_frame)
            self.masks_walk.append(pg.mask.from_surface(scaled_frame))

        # Текущее состояние
        self.current_frame_index = 0
        self.animation_timer = 0.0
        self.animation_speed = 0.1
        self.is_moving = False
        self.current_frames = self.frames_idle
        self.current_masks = self.masks_idle
        self.image = self.current_frames[0]
        self.mask = self.current_masks[0]

        # ===== РАЗМЕРЫ И КОЛЛИЗИИ =====
        self.size = new_w
        # Радиус берём чуть меньше половины ширины, чтобы избежать резких раздвиганий
        self.radius = 20    # например, 40% от ширины – подберите под свой спрайт
        # Если хотите фиксированный радиус, закомментируйте выше и раскомментируйте:
        # self.radius = 25

        self.rect = self.image.get_rect(center=(x, y))

        # ===== Характеристики =====
        self.maxHealth = 1500
        self.health = self.maxHealth
        self.speed = 150
        self.damage = 80

    def update_animation(self, dt):
        # ... без изменений (код из предыдущего ответа) ...
        if self.is_moving:
            new_frames = self.frames_walk
            new_masks = self.masks_walk
        else:
            new_frames = self.frames_idle
            new_masks = self.masks_idle

        if new_frames != self.current_frames:
            self.current_frames = new_frames
            self.current_masks = new_masks
            self.current_frame_index = 0
            self.animation_timer = 0.0
            self.image = self.current_frames[0]
            self.mask = self.current_masks[0]
            return

        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0.0
            self.current_frame_index = (self.current_frame_index + 1) % len(self.current_frames)
            self.image = self.current_frames[self.current_frame_index]
            self.mask = self.current_masks[self.current_frame_index]

    def update(self, dt):
        self.move(dt)
        self.update_animation(dt)

    def death(self):
        pass

    def collidesWith(self, other):
        if not self.rect.colliderect(other.rect):
            return False
        offsetX = other.rect.x - self.rect.x
        offsetY = other.rect.y - self.rect.y
        return self.mask.overlap(other.mask, (offsetX, offsetY)) is not None

    def move(self, dt):
        dx = self.hero.x - self.x
        dy = self.hero.y - self.y
        distance = math.hypot(dx, dy)

        if distance > 1:
            self.is_moving = True
            dx /= distance
            dy /= distance
            self.x += dx * self.speed * dt
            self.y += dy * self.speed * dt
        else:
            self.is_moving = False

        self.rect.center = (self.x, self.y)

    def draw(self, screen, camera):
        screen_pos = camera.apply(self.x, self.y)
        draw_x = screen_pos[0] - self.image.get_width() // 2
        draw_y = screen_pos[1] - self.image.get_height() // 2
        screen.blit(self.image, (draw_x, draw_y))

    def getDamage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.death()
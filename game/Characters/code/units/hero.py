from Characters.code.units.baseUnit import Unit
from Items.code.swordSlice import Sword
from constans import *
import math
import pygame as pg
import random as rd


class Warrior(Unit):
    
    def __init__(self, x, y, screen, game_field):
        super().__init__(x, y)
        self.screen = screen
        self.game_field = game_field

        # ===== Коэффициент масштабирования =====
        self.scale_factor = 1.0

        # Загрузка спрайт-листа (8 столбцов, 2 строки: idle / walk)
        self.sprite_sheet = pg.image.load(SPRITE_PATH_HERO).convert_alpha()
        orig_w = self.sprite_sheet.get_width() // 8
        orig_h = self.sprite_sheet.get_height() // 2
        new_w = int(orig_w * self.scale_factor)
        new_h = int(orig_h * self.scale_factor)

        # Кадры и маски для idle
        self.frames_idle = []
        self.masks_idle = []
        for col in range(8):
            frame = self.sprite_sheet.subsurface((col * orig_w, 0, orig_w, orig_h))
            scaled_frame = pg.transform.smoothscale(frame, (new_w, new_h))
            self.frames_idle.append(scaled_frame)
            self.masks_idle.append(pg.mask.from_surface(scaled_frame))

        # Кадры и маски для walk
        self.frames_walk = []
        self.masks_walk = []
        for col in range(8):
            frame = self.sprite_sheet.subsurface((col * orig_w, orig_h, orig_w, orig_h))
            scaled_frame = pg.transform.smoothscale(frame, (new_w, new_h))
            self.frames_walk.append(scaled_frame)
            self.masks_walk.append(pg.mask.from_surface(scaled_frame))

        # Текущее состояние анимации
        self.current_frame_index = 0
        self.animation_timer = 0.0
        self.animation_speed = 0.1          # секунд на кадр
        self.is_moving = False
        self.current_frames = self.frames_idle
        self.current_masks = self.masks_idle
        self.image = self.current_frames[0]
        self.mask = self.current_masks[0]   # маска для коллизий

        # ===== Размеры и коллизии =====
        self.size = new_w
        self.radius = 25
        self.rect = self.image.get_rect(center=(x, y))

        # ==================== Характеристики ====================
        self.level = 1
        self.maxHealth = 750
        self.health = self.maxHealth
        self.speed = 300
        self.radiusExp = 10
        self.damage = 100
        self.critChance = 0.05
        self.critMod = 1.5
        self.invincibleTimer = 0.0

        # ===== Атака =====
        self.lastMoveDir = (0, 1)
        self.prevMoveDir = (0, 1)
        self.weapon = Sword(self)

    def update_animation(self, dt):
        """Обновляет кадр и маску в зависимости от движения"""
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

        if self.lastMoveDir != self.prevMoveDir:
            self.weapon.cancelEffects()
            self.prevMoveDir = self.lastMoveDir
        else:
            self.prevMoveDir = self.lastMoveDir

        if self.invincibleTimer > 0:
            self.invincibleTimer -= dt
            if self.invincibleTimer < 0:
                self.invincibleTimer = 0

        self.weapon.update(dt)
        if self.weapon.canActivate():
            self.weapon.activate()

    def loadAttackParts(self):
        self.attackParts = []
        for i in range(1, 5):
            path = f"sprites/attack_slice_{i}.png"
            img = pg.image.load(path).convert_alpha()
            self.attackParts.append(img)

    def move(self, dt):
        keys = pg.key.get_pressed()
        move_x, move_y = 0, 0

        if keys[pg.K_w] or keys[pg.K_UP]:
            move_y -= 1
        if keys[pg.K_s] or keys[pg.K_DOWN]:
            move_y += 1
        if keys[pg.K_a] or keys[pg.K_LEFT]:
            move_x -= 1
        if keys[pg.K_d] or keys[pg.K_RIGHT]:
            move_x += 1

        self.is_moving = (move_x != 0 or move_y != 0)

        if move_x != 0 or move_y != 0:
            length = math.hypot(move_x, move_y)
            self.lastMoveDir = (move_x / length, move_y / length)

        if move_x != 0 and move_y != 0:
            move_x *= 0.707
            move_y *= 0.707

        self.x += move_x * self.speed * dt
        self.y += move_y * self.speed * dt

        # Границы с учётом размера спрайта
        half = self.size // 2
        self.x = max(half, min(self.x, self.game_field.world_width - half))
        self.y = max(half, min(self.y, self.game_field.world_height - half))

        self.rect.center = (self.x, self.y)

    def draw(self, screen, camera):
        screen_pos = camera.apply(self.x, self.y)
        draw_x = screen_pos[0] - self.image.get_width() // 2
        draw_y = screen_pos[1] - self.image.get_height() // 2
        screen.blit(self.image, (draw_x, draw_y))

        # Полоска здоровья
        bar_width, bar_height = 40, 6
        health_percent = self.health / self.maxHealth
        bar_x = screen_pos[0] - bar_width // 2
        bar_y = screen_pos[1] - self.image.get_height() // 2 - 10
        pg.draw.rect(screen, (60, 60, 60), (bar_x, bar_y, bar_width, bar_height))
        pg.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, bar_width * health_percent, bar_height))

        self.weapon.draw(screen, camera)

    def get_rect(self):
        return pg.Rect(self.x - self.size//2, self.y - self.size//2, self.size, self.size)

    def getDamage(self, damage):
        if self.invincibleTimer > 0:
            return
        self.health -= damage
        self.invincibleTimer = 0.5
        if self.health <= 0:
            self.death()

    def damageMod(self):
        if rd.random() < self.critChance:
            return self.damage * self.critMod
        return self.damage
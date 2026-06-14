from .baseItems import Weapon
from .slashEffects import SlashEffect
import pygame as pg

class Sword(Weapon):
    def __init__(self, owner):
        super().__init__(owner)
        self.damage = 25
        self.critChance = 0.1
        self.critMultiplier = 1.8
        self.cooldownTime = 0.6
        self.attackImage = self.loadImage()
        # Размеры цельного спрайта (предположим, 64×64)
        self.anim_w = self.attackImage.get_width()
        self.anim_h = self.attackImage.get_height()
        # Размер одной "виртуальной" части (было 2×2 сетка)
        self.part_w = self.anim_w // 2
        self.part_h = self.anim_h // 2

    def loadImage(self):
        path = "./Items/sprites/sword-attack.png"   # ваш цельный спрайт
        img = pg.image.load(path).convert_alpha()
        # приведите к нужному размеру (например, 64×64)
        img = pg.transform.smoothscale(img, (64, 64))
        return img

    def createEffects(self):
        direction = self.owner.lastMoveDir
        effect = SlashEffect(self.owner, self.attackImage, direction, self.getOffset)
        self.activeEffects.append(effect)

    def getOffset(self, owner, dx, dy):
        """Возвращает (x0, y0) – левый верхний угол квадрата атаки (как раньше для 4 частей)"""
        w = self.part_w
        h = self.part_h
        anim_w = w * 2
        anim_h = h * 2
        cx, cy = owner.x, owner.y
        r = owner.radius

        # Те же смещения, что были в getSlashPositions
        if dx > 0:   # вправо
            ox, oy = r + 5, -anim_h // 2
        elif dx < 0: # влево
            ox, oy = -r - anim_w - 5, -anim_h // 2
        elif dy > 0: # вниз
            ox, oy = -anim_w // 2, r + 5
        else:        # вверх
            ox, oy = -anim_w // 2, -r - anim_h - 5

        x0 = cx + ox
        y0 = cy + oy
        return (x0, y0)
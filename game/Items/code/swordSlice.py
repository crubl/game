import pygame as pg
from .baseItems import Weapon
from .slashEffects import SlashEffect

class Sword(Weapon):
    def __init__(self, owner):
        super().__init__(owner)
        self.damage = 80
        self.critChance = 0.1
        self.critMultiplier = 1.8
        self.cooldown = 0.6
        self.frames = self.loadFrames()
        self.effect_duration = 0.8

    def loadFrames(self):
        sheet = pg.image.load("./Items/sprites/attack.png").convert_alpha()
        fw = sheet.get_width() // 4
        fh = sheet.get_height() // 4
        frames = []
        for row in range(4):
            for col in range(4):
                rect = pg.Rect(col * fw, row * fh, fw, fh)
                frames.append(sheet.subsurface(rect))
        return frames

    def createEffects(self):
        direction = self.owner.lastMoveDir
        # Пропускаем первые 3 пустых кадра, берём с индекса 3
        frames_to_use = self.frames[3:] if len(self.frames) > 3 else self.frames
        if not frames_to_use:
            return
        effect = SlashEffect(
            owner=self.owner,
            frames=frames_to_use,
            direction=direction,
            offsetFunc=self.getOffset,
            total_duration=self.effect_duration
        )
        self.activeEffects.append(effect)

    def getOffset(self, owner, dx, dy):
        if not self.frames:
            return (owner.x, owner.y)
        w = self.frames[0].get_width()
        h = self.frames[0].get_height()
        cx, cy = owner.x, owner.y
        r = owner.radius if hasattr(owner, 'radius') else 30

        if dx > 0:      # вправо
            ox = r + 5
            oy = -h // 2
        elif dx < 0:    # влево
            ox = -r - w - 5
            oy = -h // 2
        elif dy > 0:    # вниз
            ox = -w // 2
            oy = r + 5
        else:           # вверх
            ox = -w // 2
            oy = -r - h - 5
        return (cx + ox, cy + oy)
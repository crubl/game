from .baseItems import Weapon
from .slashEffects import SlashEffect
import pygame as pg

class Sword(Weapon):
    def __init__(self, owner):
        super().__init__(owner)
        self.damage = 80
        self.critChance = 0.1
        self.critMultiplier = 1.8
        self.cooldown = 0.6                     # <- теперь правильно установлен
        self.attackImage = self.loadImage()
        # Размер спрайта (можно задать свой)
        self.sprite_width = self.attackImage.get_width()
        self.sprite_height = self.attackImage.get_height()

    def loadImage(self):
        path = "./Items/sprites/sword-attack.png"
        img = pg.image.load(path).convert_alpha()
        # Масштабируем до удобного размера, например 64x64
        img = pg.transform.smoothscale(img, (64, 64))
        return img

    def createEffects(self):
        direction = self.owner.lastMoveDir
        effect = SlashEffect(self.owner, self.attackImage, direction, self.getOffset)
        self.activeEffects.append(effect)

    def getOffset(self, owner, dx, dy):
        """Возвращает левый верхний угол спрайта относительно центра игрока.
           Спрайт центрируется по направлению атаки."""
        w = self.sprite_width
        h = self.sprite_height
        cx, cy = owner.x, owner.y
        r = owner.radius

        # Смещение в зависимости от направления
        # Ставим спрайт так, чтобы он был перед игроком
        if dx > 0:   # вправо
            ox = r + 5
            oy = -h // 2
        elif dx < 0: # влево
            ox = -r - w - 5
            oy = -h // 2
        elif dy > 0: # вниз
            ox = -w // 2
            oy = r + 5
        else:        # вверх
            ox = -w // 2
            oy = -r - h - 5

        return (cx + ox, cy + oy)
from .baseItems import WeaponEffect
import pygame as pg

class SlashEffect(WeaponEffect):
    def __init__(self, owner, image, direction, offsetFunc):
        super().__init__(owner)
        self.original_image = image
        self.image = image.copy()
        self.direction = direction
        self.offsetFunc = offsetFunc
        self.alpha = 0
        self.fadeSpeed = 20
        self.damagedEnemies = set()
        self.rect = self.image.get_rect()
        self.updatePosition()

    def updatePosition(self):
        # Получаем левый верхний угол квадрата атаки
        x0, y0 = self.offsetFunc(self.owner, self.direction[0], self.direction[1])
        self.rect.topleft = (x0, y0)

    def update(self, dt):
        self.alpha += self.fadeSpeed
        if self.alpha >= 255:
            self.alpha = 255
            self.finished = True
        self.image.set_alpha(self.alpha)
        # Анимация следует за героем (обновляем позицию каждый кадр)
        self.updatePosition()

    def draw(self, surface, camera):
        screen_pos = camera.apply(self.rect.x, self.rect.y)
        surface.blit(self.image, screen_pos)

    def getHitbox(self):
        return self.rect if not self.finished else None

    def onHitEnemy(self, enemy):
        if enemy in self.damagedEnemies:
            return False
        self.damagedEnemies.add(enemy)
        return True
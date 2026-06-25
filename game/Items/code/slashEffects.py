from .baseItems import WeaponEffect
import pygame as pg

class SlashEffect(WeaponEffect):
    def __init__(self, owner, image, direction, offsetFunc):
        super().__init__(owner)
        self.original_image = image
        self.image = image.copy()
        self.direction = direction
        self.offsetFunc = offsetFunc
        self.lifetime = 0.3                     # секунд, эффект активен
        self.timer = 0.0
        self.damagedEnemies = set()
        self.rect = self.image.get_rect()
        self.updatePosition()

    def updatePosition(self):
        x0, y0 = self.offsetFunc(self.owner, self.direction[0], self.direction[1])
        self.rect.topleft = (x0, y0)

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.lifetime:
            self.finished = True
        # Анимация следует за игроком
        self.updatePosition()

    def draw(self, surface, camera):
        if self.finished:
            return
        # При желании можно добавить прозрачность по времени
        # alpha = int(255 * (1 - self.timer / self.lifetime))
        # self.image.set_alpha(alpha)
        screen_pos = camera.apply(self.rect.x, self.rect.y)
        surface.blit(self.image, screen_pos)

    def getHitbox(self):
        return self.rect if not self.finished else None

    def onHitEnemy(self, enemy):
        if enemy in self.damagedEnemies:
            return False
        self.damagedEnemies.add(enemy)
        return True
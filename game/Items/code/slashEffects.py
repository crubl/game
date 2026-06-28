import pygame as pg
from .baseItems import WeaponEffect

class SlashEffect(WeaponEffect):
    def __init__(self, owner, frames, direction, offsetFunc, total_duration=0.3):
        super().__init__(owner)
        self.frames = frames if frames else []
        self.current_frame = 0
        self.frame_timer = 0.0
        self.total_duration = total_duration
        self.frame_duration = total_duration / len(self.frames) if self.frames else 0.1
        self.image = self.frames[0] if self.frames else None
        self.direction = direction
        self.offsetFunc = offsetFunc
        self.damagedEnemies = set()
        self.rect = self.image.get_rect() if self.image else pg.Rect(0, 0, 0, 0)
        self.updatePosition()

    def updatePosition(self):
        if not self.image:
            return
        x0, y0 = self.offsetFunc(self.owner, self.direction[0], self.direction[1])
        self.rect.topleft = (x0, y0)

    def update(self, dt):
        if self.finished or not self.frames:
            return
        self.frame_timer += dt
        if self.frame_timer >= self.frame_duration:
            self.frame_timer = 0.0
            self.current_frame += 1
            if self.current_frame >= len(self.frames):
                self.finished = True
                return
            self.image = self.frames[self.current_frame]
            self.rect = self.image.get_rect()
            self.updatePosition()
        self.updatePosition()  # эффект следует за игроком

    def draw(self, surface, camera):
        if self.finished or not self.image:
            return
        screen_pos = camera.apply(self.rect.x, self.rect.y)
        surface.blit(self.image, screen_pos)

    def getHitbox(self):
        if self.finished or not self.image:
            return None
        return self.rect.inflate(-6, -6)

    def onHitEnemy(self, enemy):
        if enemy in self.damagedEnemies:
            return False
        self.damagedEnemies.add(enemy)
        return True
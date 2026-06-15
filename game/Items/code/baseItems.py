import pygame as pg

class WeaponEffect:
    """Базовый класс для одного активного эффекта (удар, снаряд, аура)"""
    def __init__(self, owner):
        self.owner = owner
        self.finished = False

    def update(self, dt):
        pass

    def draw(self, surface, camera):
        pass

    def isFinished(self):
        return self.finished

    def getHitbox(self):
        return None

    def onHitEnemy(self, enemy):
        pass


class Weapon:
    """Базовый класс для всего оружия"""
    def __init__(self, owner):
        self.owner = owner
        self.cooldown = 0.8          # базовая задержка (секунд)
        self.currentCooldown = 0.0       # текущий оставшийся кулдаун
        self.activeEffects = []          # список активных эффектов

    def cancelEffects(self):
        """Немедленно завершает все активные эффекты атаки"""
        for effect in self.activeEffects[:]:
            effect.finished = True
        self.activeEffects.clear()
        
    def canActivate(self):
        return self.currentCooldown <= 0.0

    def activate(self, ignoreCooldown=False):
        if not ignoreCooldown and not self.canActivate():
            return False
        if not ignoreCooldown:
            self.currentCooldown = self.cooldown
        self.createEffects()
        return True

    def createEffects(self):
        pass

    def update(self, dt):
        if self.currentCooldown > 0:
            self.currentCooldown -= dt

        for effect in self.activeEffects[:]:
            effect.update(dt)
            if effect.isFinished():
                self.activeEffects.remove(effect)

    def draw(self, surface, camera):
        for effect in self.activeEffects:
            effect.draw(surface, camera)

    def getActiveHitboxes(self):
        boxes = []
        for effect in self.activeEffects:
            rect = effect.getHitbox()
            if rect:
                boxes.append((effect, rect))
        return boxes
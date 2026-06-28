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
    """Базовый класс для всего оружия с кулдауном после анимации"""
    def __init__(self, owner):
        self.owner = owner
        self.cooldown = 0.8          # базовая задержка (секунд)
        self.currentCooldown = 0.0   # текущий оставшийся кулдаун
        self.activeEffects = []      # список активных эффектов
        self.is_animating = False    # флаг, что идёт анимация атаки

    def cancelEffects(self):
        """Немедленно завершает все активные эффекты атаки"""
        for effect in self.activeEffects[:]:
            effect.finished = True
        self.activeEffects.clear()
        self.is_animating = False

    def canActivate(self):
        """Можно активировать, если нет анимации и кулдаун <= 0"""
        return (not self.is_animating) and (self.currentCooldown <= 0.0)

    def activate(self, ignoreCooldown=False):
        """Активирует оружие, запускает анимацию и устанавливает кулдаун"""
        if not ignoreCooldown and not self.canActivate():
            return False
        if not ignoreCooldown:
            self.currentCooldown = self.cooldown
        self.is_animating = True
        self.createEffects()
        return True

    def createEffects(self):
        """Переопределяется в наследниках для создания эффектов"""
        pass

    def update(self, dt):
        #Обновляем активные эффекты, удаляем завершённые
        for effect in self.activeEffects[:]:
            effect.update(dt)
            if effect.isFinished():
                self.activeEffects.remove(effect)

        #Если анимация была активна и все эффекты завершились – снимаем флаг
        if self.is_animating and not self.activeEffects:
            self.is_animating = False

        #Уменьшаем кулдаун только если анимация завершена (или её нет)
        if not self.is_animating and self.currentCooldown > 0:
            self.currentCooldown -= dt
            if self.currentCooldown < 0:
                self.currentCooldown = 0.0

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
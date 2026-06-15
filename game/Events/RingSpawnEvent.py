# Events/RingSpawnEvent.py

"""
Ивент: спавн кольца врагов вокруг игрока
"""

import math
from .BaseEvent import BaseEvent


class RingSpawnEvent(BaseEvent):
    """Спавнит кольцо врагов вокруг игрока"""
    
    def __init__(self, trigger_time: float, enemy_count: int, radius: int, enemy_class, speed_multiplier: float = 1.0):
        """
        trigger_time - время спавна (секунды)
        enemy_count - количество врагов в кольце
        radius - радиус кольца (пиксели от центра)
        enemy_class - класс врага (например, Walker)
        speed_multiplier - множитель скорости врагов (1.0 = обычная скорость)
        """
        super().__init__(trigger_time)
        self.enemy_count = enemy_count
        self.radius = radius
        self.enemy_class = enemy_class
        self.speed_multiplier = speed_multiplier
    
    def execute(self, game_field):
        """Создаёт кольцо врагов вокруг игрока"""
        if not game_field.player:
            return
        
        center_x = game_field.player.x
        center_y = game_field.player.y
        
        for i in range(self.enemy_count):
            # Вычисляем позицию каждого врага по кругу
            angle = (2 * math.pi / self.enemy_count) * i
            x = center_x + math.cos(angle) * self.radius
            y = center_y + math.sin(angle) * self.radius
            
            # Ограничиваем границами мира
            x = max(0, min(x, game_field.world_width))
            y = max(0, min(y, game_field.world_height))
            
            # Создаём врага
            enemy = self.enemy_class(x, y, game_field.player, game_field.screen)

            # Применяем множитель скорости
            if self.speed_multiplier != 1.0:
                enemy.speed = int(enemy.speed * self.speed_multiplier)
                
            game_field.enemies.append(enemy)
        
        print(f"[Ивент] Кольцевой спавн: {self.enemy_count} врагов, радиус {self.radius}, скорость x{self.speed_multiplier}")
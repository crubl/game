import pygame as pg


class Camera:
    
    def __init__(self, screen_width, screen_height, world_width, world_height):
        # Размеры экрана и мира
        self.screen_width = screen_width      # ширина экрана в пикселях
        self.screen_height = screen_height    # высота экрана в пикселях
        self.world_width = world_width        # ширина игрового мира
        self.world_height = world_height      # высота игрового мира
        
        # Позиция камеры в мировых координатах (левый верхний угол)
        self.x = 0.0
        self.y = 0.0
    
    def update(self, target_x, target_y):
        """Центрирует камеру на цели и ограничивает границами мира"""
        # Центрируем камеру на игроке
        self.x = target_x - self.screen_width // 2
        self.y = target_y - self.screen_height // 2
        
        # Не выходим за границы мира (левая и верхняя граница)
        self.x = max(0, self.x)
        self.y = max(0, self.y)
        
        # Не выходим за границы мира (правая и нижняя граница)
        self.x = min(self.x, self.world_width - self.screen_width)
        self.y = min(self.y, self.world_height - self.screen_height)
    
    def apply(self, x, y):
        """
        Переводит мировые координаты в экранные (с учётом камеры)
        Используется для отрисовки объектов
        """
        return (x - self.x, y - self.y)
    
    def apply_rect(self, rect):
        """Переводит прямоугольник в экранные координаты"""
        return pg.Rect(
            rect.x - self.x,
            rect.y - self.y,
            rect.width,
            rect.height
        )
    
    def is_visible(self, x, y, margin=50):
        """
        Проверяет, находится ли объект в видимой области камеры
        margin - запас за пределами экрана (чтобы объекты не исчезали у границ)
        Используется для оптимизации отрисовки
        """
        return (self.x - margin < x < self.x + self.screen_width + margin and
                self.y - margin < y < self.y + self.screen_height + margin)
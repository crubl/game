from constans import *
import pygame as pg

class Map():
    """Клас карты для поля. Создан для работы с юнитами"""
    def __init__(self, cellSize):
        self.cellSize = cellSize
        self.poly = {}

    def clear(self):
        self.poly.clear()

    def key(self, x, y):
        return (int(x // self.cellSize), int(y // self.cellSize))

    def add(self, unit):
        key = self.key(unit.x, unit.y)
        if key not in self.poly:
            self.poly[key] = []
        self.poly[key].append(unit)

    def getNearby(self, unit):
        x, y = self.key(unit.x, unit.y)
        result = []
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                key = (x + dx, y + dy)
                if key in self.poly:
                    result.extend(self.poly[key])
        return result

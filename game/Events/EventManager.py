# Events/EventManager.py
"""
Менеджер ивентов — управляет всеми событиями по таймеру
"""

from .BaseEvent import BaseEvent


class EventManager:
    #Управляет выполнением ивентов по времени
    
    def __init__(self):
        self.events = []      # список всех ивентов
        self.game_time = 0.0  # текущее игровое время
    
    def add_event(self, event: BaseEvent):
        #Добавляет один ивент
        self.events.append(event)
    
    def add_events(self, events: list):
        #Добавляет несколько ивентов
        self.events.extend(events)
    
    def clear(self):
        #Очищает все ивенты
        self.events.clear()
        self.game_time = 0.0
    
    def reset(self):
        #Сбрасывает время и помечает все ивенты как невыполненные
        self.game_time = 0.0
        for event in self.events:
            event.executed = False
    
    def update(self, dt: float, game_field):
        """
        Обновляет менеджер ивентов (вызывается каждый кадр)
        dt - время между кадрами
        game_field - ссылка на игровое поле
        """
        self.game_time += dt
        
        for event in self.events:
            event.check_and_execute(self.game_time, game_field)
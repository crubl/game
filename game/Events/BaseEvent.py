# Events/BaseEvent.py

"""
Базовый класс для всех игровых ивентов
"""

class BaseEvent:
    #Абстрактный базовый класс для ивентов
    def __init__(self, trigger_time: float):
        #trigger_time - время в секундах, когда нужно выполнить ивент
        self.trigger_time = trigger_time
        self.executed = False
    
    def check_and_execute(self, current_time: float, game_field):
        #Проверяет, нужно ли выполнить ивент
        if not self.executed and current_time >= self.trigger_time:
            self.execute(game_field)
            self.executed = True
    
    def execute(self, game_field):
        #Выполняет ивент (будет перераспределяться в других классах)
        raise NotImplementedError("Метод execute должен быть переопределён")
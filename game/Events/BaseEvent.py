"""
Базовый класс для всех игровых ивентов
"""

class BaseEvent:
    """Абстрактный базовый класс для ивентов"""
    
    def __init__(self, trigger_time: float, repeat: bool = False, interval: float = 0):
        """
        trigger_time - время в секундах, когда нужно выполнить ивент
        repeat - повторять ли ивент
        interval - интервал между повторениями (если repeat=True)
        """
        self.trigger_time = trigger_time
        self.repeat = repeat
        self.interval = interval
        self.next_trigger_time = trigger_time
        self.active = True  # активен ли ивент (если не повторяется и выполнен - False)
    
    def check_and_execute(self, current_time: float, game_field):
        """
        Проверяет, нужно ли выполнить ивент, и выполняет если нужно
        """
        # Если ивент неактивен — пропускаем
        if not self.active:
            return
        
        # Проверяем, пришло ли время выполнения
        if current_time >= self.next_trigger_time:
            self.execute(game_field)
            
            # Если ивент повторяющийся — планируем следующее выполнение
            if self.repeat and self.interval > 0:
                self.next_trigger_time = current_time + self.interval
                print(f"[Ивент] Следующий повтор через {self.interval} секунд")
            else:
                # Если не повторяющийся — деактивируем
                self.active = False
                print(f"[Ивент] Ивент завершён (не повторяется)")
    
    def execute(self, game_field):
        """
        Выполняет ивент (переопределяется в дочерних классах)
        """
        raise NotImplementedError("Метод execute должен быть переопределён")
    
    def reset(self):
        """Сбрасывает ивент для новой игры"""
        self.next_trigger_time = self.trigger_time
        self.active = True
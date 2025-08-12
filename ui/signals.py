from PySide6.QtCore import QObject, Signal

class AppSignals(QObject):
    """
    Сигналы для связи между интерфейсом и основной логикой
    """
    # Выбор микрофона
    microphone_selected = Signal(int)
    
    # Сообщения в чат
    system_message = Signal(str)  # Системные сообщения
    user_message = Signal(str)    # Сообщения от пользователя
    ai_message = Signal(str)      # Ответы ИИ
    
    # Состояние приложения
    listening_changed = Signal(bool)  # Изменение состояния прослушивания

signals = AppSignals() 
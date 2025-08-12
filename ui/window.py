from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QLabel,
    QVBoxLayout, QHBoxLayout, QScrollArea, QLineEdit, QComboBox
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap
from .widgets import MicrophoneSelector
from PySide6.QtCore import Signal
import sounddevice as sd
from ui.signals import signals


class ScaledPixmapLabel(QLabel):
    def __init__(self, pixmap, parent=None):
        super().__init__(parent)
        self.original_pixmap = pixmap
        self.setAlignment(Qt.AlignCenter)
        self.setMinimumSize(200, 200)  # минимальный размер для виджета

    def resizeEvent(self, event):
        if self.original_pixmap:
            scaled = self.original_pixmap.scaled(
                self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            self.setPixmap(scaled)
        super().resizeEvent(event)


class LuxUI(QMainWindow):

    microphone_selected = Signal(int)

    def __init__(self):
        super().__init__()
        self.signals = signals
        self.setWindowTitle("Lux Assistant")
        self.resize(1300, 750)

        self.signals.user_message.connect(lambda msg: self.add_message(msg, sender="user"))
        self.signals.ai_message.connect(lambda msg: self.add_message(msg, sender="ai"))
        self.signals.system_message.connect(lambda msg: self.add_message(msg, sender="system"))

        # ===== Левое меню =====
        left_menu = QVBoxLayout()
        btn_plugins = QPushButton("ПЛАГИНЫ")
        btn_dummy = QPushButton("ПУСТЫШКА")

        for btn in (btn_plugins, btn_dummy):
            btn.setFixedHeight(45)
            btn.setStyleSheet(self.side_button_style())

        left_menu.addWidget(btn_plugins)
        left_menu.addWidget(btn_dummy)
        left_menu.addStretch()

        left_menu_widget = QWidget()
        left_menu_widget.setLayout(left_menu)
        left_menu_widget.setFixedWidth(150)
        left_menu_widget.setStyleSheet("background-color: #0D0D0D;")

        # ===== Чат =====
        chat_layout = QVBoxLayout()

        self.chat_area = QScrollArea()
        self.chat_area.setWidgetResizable(True)
        self.chat_content = QWidget()
        self.chat_content_layout = QVBoxLayout(self.chat_content)
        self.chat_content_layout.addStretch()
        self.chat_area.setWidget(self.chat_content)

        # Поле ввода и кнопки
        input_layout = QHBoxLayout()  # Сначала создаём layout

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Введите сообщение...")
        self.input_field.setFixedHeight(50)
        self.input_field.setStyleSheet(self.input_style())

        self.send_button = QPushButton("➤")
        self.send_button.setFixedSize(50, 50)
        self.send_button.setStyleSheet(self.round_button_style("#FFD700"))

        self.mic_button = QPushButton("🎤")
        self.mic_button.setFixedSize(50, 50)
        self.mic_button.setStyleSheet(self.round_button_style("#FFD700"))

        # Добавляем основные виджеты в input_layout
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.send_button)
        input_layout.addWidget(self.mic_button)

        # Создаем селектор микрофонов после кнопки
        self.mic_selector = QComboBox()
        self.mic_selector.setFixedHeight(50)
        self.mic_selector.setFixedWidth(180)
        self.mic_selector.setStyleSheet("""
            QComboBox {
                background-color: #1A1A1A;
                color: white;
                border: 2px solid #FFD700;
                border-radius: 10px;
                padding-left: 8px;
                font-size: 14px;
            }
        """)

        # Заполняем список микрофонов
        self.update_mic_list()

        # Связываем сигнал изменения выбора с сигналом класса
        self.mic_selector.currentIndexChanged.connect(self.microphone_selected.emit)

        # Добавляем селектор микрофонов в layout
        input_layout.addWidget(self.mic_selector)

        # Добавляем чат и поле ввода в главный чатовый layout
        chat_layout.addWidget(self.chat_area)
        chat_layout.addLayout(input_layout)

        chat_widget = QWidget()
        chat_widget.setLayout(chat_layout)

        # ===== 3D модель (заглушка с картинкой и рамкой) =====
        pixmap = QPixmap("aiease_1753106626225.jpg")
        self.view3d_label = ScaledPixmapLabel(pixmap)

        # Обернем в контейнер с рамкой
        view3d_container = QWidget()
        view3d_container.setStyleSheet("""
            background-color: #111111;
            border: 3px solid #FFD700;
            border-radius: 10px;
        """)
        container_layout = QVBoxLayout(view3d_container)
        container_layout.setContentsMargins(8, 8, 8, 8)
        container_layout.addWidget(self.view3d_label)

        # ===== Основная разметка =====
        main_layout = QHBoxLayout()
        main_layout.addWidget(left_menu_widget)  # фиксированная ширина
        main_layout.addWidget(chat_widget, 3.5)
        main_layout.addWidget(view3d_container, 2.5)

        container = QWidget()
        container.setLayout(main_layout)
        container.setStyleSheet(self.main_style())
        self.setCentralWidget(container)

    def update_mic_list(self):
        import sounddevice as sd
        self.mic_selector.clear()
        devices = sd.query_devices()
        for i, dev in enumerate(devices):
            if dev['max_input_channels'] > 0:
                self.mic_selector.addItem(f"{i}: {dev['name']}", i)

    def add_message(self, text, sender="system"):
        # Создаем QLabel с текстом
        label = QLabel(text)
        label.setWordWrap(True)
        label.setTextInteractionFlags(Qt.TextSelectableByMouse)  # чтобы можно было выделить текст
        label.setStyleSheet("font-size: 16px;")

        # Создаем контейнер для выравнивания
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(10, 5, 10, 5)  # отступы вокруг текста
        layout.setSpacing(0)

        # Стилизация и выравнивание по sender
        if sender == "user":
            label.setStyleSheet("""
                background-color: #555555;
                color: white;
                padding: 8px 12px;
                border-radius: 12px;
                font-size: 16px;
            """)
            layout.addWidget(label, 0, Qt.AlignLeft)
            layout.addStretch()  # чтобы блок прижимался к левому краю

        elif sender == "ai":
            label.setStyleSheet("""
                background-color: #333333;
                color: #FFD700;
                padding: 8px 12px;
                border-radius: 12px;
                font-size: 16px;
            """)
            layout.addStretch()  # чтобы блок прижимался к правому краю
            layout.addWidget(label, 0, Qt.AlignRight)

        else:  # system или другие
            label.setStyleSheet("""
                color: #AAAAAA;
                font-style: italic;
                font-size: 14px;
                padding: 4px 6px;
            """)
            layout.addWidget(label, 0, Qt.AlignCenter)

        # Вставляем в основной layout перед stretch, чтобы сообщения шли сверху вниз
        self.chat_content_layout.insertWidget(self.chat_content_layout.count() - 1, container)

    def main_style(self):
        return """
        QWidget {
            background-color: #0A0A0A;
            color: white;
            font-size: 14px;
        }
        QScrollArea {
            background: transparent;
            border: none;
        }
        """

    def side_button_style(self):
        return """
        QPushButton {
            background-color: #1A1A1A;
            border: 2px solid #FFD700;
            color: white;
            border-radius: 8px;
            font-size: 14px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #FFD700;
            color: black;
        }
        """

    def input_style(self):
        return """
        QLineEdit {
            background-color: #1A1A1A;
            border: 2px solid #FFD700;
            border-radius: 10px;
            padding-left: 10px;
            color: white;
            font-size: 16px;
        }
        """

    def round_button_style(self, color):
        return f"""
        QPushButton {{
            background-color: {color};
            border: none;
            border-radius: 25px;
            color: black;
            font-weight: bold;
            font-size: 18px;
        }}
        QPushButton:hover {{
            background-color: white;
            color: {color};
        }}
        """

import asyncio
from PySide6.QtWidgets import QApplication

class AsyncApp:
    def __init__(self):
        self.app = QApplication([])
        self.main_window = LuxUI()
        self.main_window.show()
        
    async def run(self):
        # Запускаем Qt event loop вместе с asyncio
        while True:
            self.app.processEvents()
            await asyncio.sleep(0.01)

if __name__ == "__main__":
    app = QApplication([])
    window = LuxUI()
    window.show()
    app.exec()
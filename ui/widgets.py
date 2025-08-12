from PySide6.QtWidgets import QLabel, QComboBox
from PySide6.QtCore import Qt

class MicrophoneSelector(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QComboBox {
                background-color: #1A1A1A;
                color: white;
                border: 1px solid #FFD700;
                padding: 5px;
                border-radius: 5px;
            }
        """)

class ChatMessage(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("color: white; font-size: 14px;")
        self.setWordWrap(True)
        self.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
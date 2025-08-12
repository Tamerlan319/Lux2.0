import asyncio
import sys
from PySide6.QtWidgets import QApplication
from ui.window import LuxUI

class LuxApp:
    def __init__(self):
        self.qt_app = QApplication([])
        self.window = LuxUI()
        self.window.destroyed.connect(self.stop)  # Когда окно уничтожено — останавливаем
        self.running = True

    def stop(self):
        """Остановка приложения"""
        self.running = False

    async def run(self):
        """Запуск главного цикла"""
        self.window.show()
        while self.running:
            self.qt_app.processEvents()
            await asyncio.sleep(0.01)

        print("Закрываем asyncio и выходим...")
        sys.exit(0)  # Полное завершение процесса

async def run_all():
    app = LuxApp()
    await app.run()

if __name__ == "__main__":
    try:
        asyncio.run(run_all())
    except Exception as e:
        print(f"Ошибка: {e}")

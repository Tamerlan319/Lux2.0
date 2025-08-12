import asyncio
from PySide6.QtWidgets import QApplication
from ui.window import LuxUI
from main.starter import main as lux_main

class AsyncApp:
    def __init__(self):
        self.app = QApplication([])
        self.window = LuxUI()
        self.window.show()
        self.task = None

    async def run(self):
        # Запускаем фоновой таск прослушивания и обработки
        self.task = asyncio.create_task(lux_main())

        while True:
            self.app.processEvents()
            await asyncio.sleep(0.01)
            # Можно здесь добавить проверку task и обработку исключений

async def run_all():
    async_app = AsyncApp()
    await async_app.run()

if __name__ == "__main__":
    try:
        asyncio.run(run_all())
    except Exception as e:
        print(f"Ошибка: {e}")

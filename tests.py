import unittest
from unittest.mock import AsyncMock, patch
import asyncio
from plugins.plugin import count_handler, stop_count_handler, background_tasks
from main import MyBotAPI

class TestCountHandler(unittest.IsolatedAsyncioTestCase):  # Используем IsolatedAsyncioTestCase для асинхронных тестов

    @patch.object(MyBotAPI, 'say', new_callable=AsyncMock)  # Мокаем метод say
    async def test_count_handler_start(self, mock_say):
        api = MyBotAPI()  # Создаем объект api, используя MyBotAPI
        cmd = 'считай'  # Команда для старта счёта

        await count_handler(api, cmd)  # Запуск асинхронной функции

        # Даем время для начала выполнения задачи
        await asyncio.sleep(0.1)  # Подождать немного, чтобы задача успела начать

        # Проверяем, что сообщение "Начинаю считать" было отправлено
        mock_say.assert_called_with("Начинаю считать")

        # Проверяем, что задача была добавлена в background_tasks
        self.assertIn('count', background_tasks)

        # Проверяем, что задача не завершена
        self.assertFalse(background_tasks['count'].done())  # Задача не должна быть завершена

    @patch.object(MyBotAPI, 'say', new_callable=AsyncMock)  # Мокаем метод say
    async def test_stop_count_handler(self, mock_say):
        api = MyBotAPI()  # Создаем объект api, используя MyBotAPI

        # Имитируем, что задача уже была созданаd
        task = asyncio.create_task(asyncio.sleep(10))  # Создаем задачу в активном цикле
        background_tasks['count'] = task

        # Запуск обработчика остановки счёта с использованием asyncio.run
        await stop_count_handler(api, 'останови счёт')  # Запуск асинхронной функции

        # Проверяем, что задача была отменена
        self.assertNotIn('count', background_tasks)  # Задача должна быть удалена
        mock_say.assert_called_with("Счёт остановлен")

if __name__ == '__main__':
    unittest.main()

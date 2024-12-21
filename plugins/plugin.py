#plugin.py
import asyncio
from core import BotAPI, CommandRouter, background_tasks

router = CommandRouter()

@router('считай')
async def count_handler(api: BotAPI, cmd: str):
    async def count_task():
        print("Начинаю считать...")
        try:
            i = 1
            await api.say("Начинаю считать")
            while True:
                print(f'{i}')
                i += 1
                await asyncio.sleep(1.0)
        except asyncio.CancelledError:
            print("Счётчик остановлен")

    task = asyncio.create_task(count_task())
    background_tasks['count'] = task


@router('останови счёт')
async def stop_count_handler(api: BotAPI, cmd: str):
    task = background_tasks.pop('count', None)
    if task:
        task.cancel()
        await api.say("Счёт остановлен")
    else:
        await api.say("Счёт не запущен")

@router('расскажи анекдот')
async def tell_joke(api: BotAPI, cmd: str):
    await api.say("Вот анекдот: Колобок повесился.")

@router('останови всё')
async def stop_all_tasks(api: BotAPI, cmd: str):
    if background_tasks:
        for task_name, task in list(background_tasks.items()):  # Копируем словарь, чтобы избежать изменения во время итерации
            task.cancel()  # Завершаем задачу
            await asyncio.sleep(0)  # Даем шанс обработать завершение
        background_tasks.clear()  # Очищаем все задачи
        await api.say("Все задачи остановлены.")
    else:
        await api.say("Нет активных задач.")

@router('покажи задачи')
async def show_tasks(api: BotAPI, cmd: str):
    if background_tasks:
        tasks_list = "\n".join(background_tasks.keys())
        print(f"Активные задачи:\n{tasks_list}")
    else:
        await api.say("Нет активных задач.")

import webbrowser
import urllib.parse

@router('найди в интернете')
async def search_web(api: BotAPI, cmd: str):
    print("Начинаю поиск...")
    # Разделяем строку на части по словам "найди в интернете"
    parts = cmd.split("найди в интернете", 1)
    if len(parts) < 2:
        return ""  # Если слов "найди в интернете" нет в строке, возвращаем пустую строку
    # Берем часть строки после слов "найди в интернете"
    query = parts[1].strip()
    # Кодируем данные для использования в URL
    encoded_query = urllib.parse.quote(query)
    # Формируем URL для поиска в Google
    search_url = f'https://www.google.com/search?q={encoded_query}'
    # Открываем веб-браузер с результатами поиска
    webbrowser.open(search_url, new=2)
    await api.say("Вот что мне удалось найти")

@router('открой браузер')
async def browser(api: BotAPI, cmd: str):
    await api.say("Открываю")
    webbrowser.open('https://', new=2)
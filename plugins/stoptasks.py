import asyncio
from plugins import router, BotAPI, background_tasks

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
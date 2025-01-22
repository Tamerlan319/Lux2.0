import asyncio
from plugins import router, BotAPI, background_tasks

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
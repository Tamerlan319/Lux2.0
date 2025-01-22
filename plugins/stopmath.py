from plugins import router, BotAPI, background_tasks

@router('останови счёт')
async def stop_count_handler(api: BotAPI, cmd: str):
    task = background_tasks.pop('count', None)
    if task:
        task.cancel()
        await api.say("Счёт остановлен")
    else:
        await api.say("Счёт не запущен")
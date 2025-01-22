from plugins import router, BotAPI, background_tasks

@router('покажи задачи')
async def show_tasks(api: BotAPI, cmd: str):
    if background_tasks:
        tasks_list = "\n".join(background_tasks.keys())
        print(f"Активные задачи:\n{tasks_list}")
    else:
        await api.say("Нет активных задач.")
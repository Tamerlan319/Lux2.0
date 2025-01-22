from plugins import router, BotAPI

@router('расскажи анекдот')
async def tell_joke(api: BotAPI, cmd: str):
    await api.say("Вот анекдот: Колобок повесился.")
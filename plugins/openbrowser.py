from plugins import router, BotAPI
import webbrowser

@router('открой браузер')
async def browser(api: BotAPI, cmd: str):
    await api.say("Открываю")
    webbrowser.open('https://', new=2)
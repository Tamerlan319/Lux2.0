from plugins import router, BotAPI
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
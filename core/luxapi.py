from .skeleton import BotAPI, Avatar, CommandRouter
import typing
from typing import Callable, Awaitable
from .speaker.text_to_speech import speak as default_speak

background_tasks = {}

class Lux(BotAPI, Avatar):
    def __init__(self, speakMethod: Callable[[str], Awaitable[None]] = default_speak):
        self.speakMethod = speakMethod
    
    async def say(self, text: str) -> None:
        try:
            await self.speakMethod(text)
        except Exception as e:
            print(f"Ошибка синтеза речи: {e}")

    def register(self, router: CommandRouter) -> None:
        self.router = router
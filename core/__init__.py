import typing as t
from text_to_speech import speak

background_tasks = {}

class BotAPI(t.Protocol):
    def register(self, router: 'CommandRouter') -> None:
        pass

    async def say(self, text: str) -> None:
        pass

CommandHandler = t.Callable[[BotAPI, str], t.Awaitable[None]]
CommandPredicate = t.Callable[[str], bool]

class CommandRouter:
    def __init__(self):
        self._handlers: list[tuple[CommandPredicate, CommandHandler]] = []

    def __call__(self, arg: str) -> t.Callable[[CommandHandler], CommandHandler]:
        def predicate(cmd: str):
            return arg in cmd

        def decorator(func: CommandHandler) -> CommandHandler:
            self._handlers.append((predicate, func))
            return func

        return decorator

    def try_run(self, cmd: str) -> t.Optional[CommandHandler]:
        for predicate, handler in self._handlers:
            if predicate(cmd):
                return handler
        return None

class MyBotAPI(BotAPI):
     async def say(self, text: str) -> None:
         await speak(text)

     def register(self, router: CommandRouter) -> None:
         pass
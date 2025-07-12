import typing
from typing import Protocol

class BotAPI(Protocol):
    def register(self, router: 'CommandRouter') -> None:
        pass

    async def say(self, text: str) -> None:
        pass

CommandHandler = typing.Callable[[BotAPI, str], typing.Awaitable[None]]
CommandPredicate = typing.Callable[[str], bool]

class CommandRouter:
    def __init__(self):
        self._handlers: list[tuple[CommandPredicate, CommandHandler]] = []

    def __call__(self, arg: str) -> typing.Callable[[CommandHandler], CommandHandler]:
        def predicate(cmd: str):
            return arg in cmd

        def decorator(func: CommandHandler) -> CommandHandler:
            self._handlers.append((predicate, func))
            return func

        return decorator

    def try_run(self, cmd: str) -> typing.Optional[CommandHandler]:
        for predicate, handler in self._handlers:
            if predicate(cmd):
                return handler
        return None
    
class Avatar:
    def struct(self) -> None:
        pass
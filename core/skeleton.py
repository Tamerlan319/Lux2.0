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
        self._exact_commands = {'давай поговорим', 'закончи диалог'}

    def __call__(self, arg: str) -> typing.Callable[[CommandHandler], CommandHandler]:
        def predicate(cmd: str):
            cmd = cmd.strip().lower()
            # Для специальных команд ИИ-чата требуем точного совпадения
            if arg in self._exact_commands:
                return arg == cmd
            # Для wildcard обработчика
            if arg == '*':
                return True
            # Для всех остальных команд проверяем наличие ключевой фразы
            return arg in cmd

        def decorator(func: CommandHandler) -> CommandHandler:
            self._handlers.append((predicate, func))
            return func

        return decorator

    async def execute_command(self, api: BotAPI, cmd: str) -> bool:
        """Улучшенная версия execute_command"""
        if not cmd:
            return False
            
        cmd_lower = cmd.strip().lower()
        
        # Сортируем обработчики: сначала точные, потом частичные, потом wildcard
        handlers_order = sorted(
            self._handlers,
            key=lambda x: (
                0 if x[0] in self._exact_commands else 
                1 if x[1].__name__ != 'handle_chat_message' else 
                2
            )
        )
        
        for predicate, handler in handlers_order:
            if predicate(cmd_lower):
                try:
                    await handler(api, cmd)
                    return True
                except Exception as e:
                    print(f"Ошибка выполнения команды {handler.__name__}: {e}")
                    return True
        return False
    
class Avatar:
    def struct(self) -> None:
        pass
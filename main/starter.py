import asyncio
import sounddevice as sd
from vosk import KaldiRecognizer
import json
from .settings import vosk_model
from .config import LUX_API, Q, SAMPLERATE, DEVICE
from plugins import router
from .words import triggers, recognize_command
from plugins.ai_chat_mode import ai_chat  # Импортируем глобальный экземпляр
from ui.signals import signals

def is_valid_command(command: str) -> bool:
    """Проверяет, является ли команда значимой (не пустая и не только триггер)."""
    words = command.split()
    return any(word not in triggers for word in words)

def listen() -> str:
    """Слушает и возвращает распознанный текст."""
    def callback(indata, frames, time, status):
        Q.put(bytes(indata))

    with sd.RawInputStream(samplerate=SAMPLERATE, 
                         blocksize=16000, 
                         device=DEVICE,
                         dtype='int16', 
                         channels=1,
                         callback=callback):
        rec = KaldiRecognizer(vosk_model, SAMPLERATE)
        while True:
            data = Q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                return result.get("text", "").lower()

async def main():
    LUX_API.register(router)
    await LUX_API.say("Привет! Я Люкс.")
    signals.system_message.emit("Ассистент запущен и готов к работе")
    
    while True:
        print("Слушаем...")
        text = await asyncio.get_event_loop().run_in_executor(None, listen)

        # Сначала проверяем режим диалога с ИИ
        if ai_chat.active:
            # Используем execute_command вместо try_run
            handled = await router.execute_command(LUX_API, text)
            if text != "":
                signals.user_message.emit(f"Пользователь: {text}")
            if handled:
                continue
        
        # Обычная обработка команд
        if text and any(trigger in text for trigger in triggers):
            # Убираем все триггеры из текста
            for trigger in triggers:
                text = text.replace(trigger, "").strip()

            if not is_valid_command(text):
                print("Только триггер. Жду полноценной команды.")
                continue

            command = recognize_command(text)
            if command:
                # Здесь тоже используем execute_command
                handled = await router.execute_command(LUX_API, command)
                if not handled:
                    await LUX_API.say("Команда не распознана.")
            else:
                await LUX_API.say("Команда не распознана. Попробуйте сказать иначе.")
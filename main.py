# main.py
import asyncio
import os
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import pyaudio
import queue
import json
from words import TRIGGERS, recognize_command
from core import MyBotAPI
import importlib
from plugins import router

# Динамическая загрузка плагинов
plugins_dir = 'plugins'
for filename in os.listdir(plugins_dir):
    if filename.endswith('.py') and filename != '__init__.py':
        module_name = filename[:-3]
        importlib.import_module(f'{plugins_dir}.{module_name}')

api = MyBotAPI()

# Настройки устройства и частоты
device = sd.default.device
samplerate = int(sd.query_devices(device[0], 'input')['default_samplerate'])  # получаем частоту микрофона
q = queue.Queue()

# Настройки Vosk
vosk_model_path = "model"
if not os.path.exists(vosk_model_path):
    raise Exception(f"Модель Vosk не найдена по пути: {vosk_model_path}")

vosk_model = Model(vosk_model_path)
p = pyaudio.PyAudio()

def is_valid_command(command: str) -> bool:
    """Проверяет, является ли команда значимой (не пустая и не только триггер)."""
    words = command.split()
    # Команда должна содержать слова кроме триггера
    return any(word not in TRIGGERS for word in words)

def listen() -> str:
    """Слушает и возвращает распознанный текст."""
    def callback(indata, frames, time, status):
        q.put(bytes(indata))

    with sd.RawInputStream(samplerate=samplerate, blocksize=16000, device=device[0], dtype='int16', channels=1,
                           callback=callback):
        rec = KaldiRecognizer(vosk_model, samplerate)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                return result.get("text", "").lower()

async def main():
    api.register(router)
    await api.say("Привет! я Люкс! ваш ассистент!")
    while True:
        text = await asyncio.get_event_loop().run_in_executor(None, listen)

        if text and any(trigger in text for trigger in TRIGGERS):
            # Убираем триггер из текста
            for trigger in TRIGGERS:
                text = text.replace(trigger, "").strip()

            # Проверяем, содержит ли текст осмысленную команду
            if not is_valid_command(text):
                print("Только триггер. Жду полноценной команды.")
                continue

            # Преобразование текста и распознавание команды
            command = recognize_command(text)
            if command:
                handler = router.try_run(command)
                if handler:
                    await handler(api, text)
                    print(f"Распознана команда: {command} - с текстом: {text}")  # Добавляем эту строку
                else:
                    await api.say("Команда не распознана.")
            else:
                await api.say("Команда не распознана. Попробуйте сказать иначе.")

# Запуск основной функции
if __name__ == "__main__":
    asyncio.run(main())

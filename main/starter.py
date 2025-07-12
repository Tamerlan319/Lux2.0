import asyncio
import sys
import os
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import json
import importlib
from plugins import router
from .config import LUX_API, PLUGINS_DIR, VOSK_MODEL_PATCH, Q
from .words import TRIGGERS, recognize_command

for filename in os.listdir(PLUGINS_DIR):
    if filename.endswith('.py') and filename != '__init__.py':
        module_name = filename[:-3]
        importlib.import_module(f'{PLUGINS_DIR}.{module_name}')

if not os.path.exists(VOSK_MODEL_PATCH):
    raise Exception(f"Модель Vosk не найдена по пути: {VOSK_MODEL_PATCH}")

vosk_model = Model(VOSK_MODEL_PATCH)

def select_microphone():
    """Функция для выбора микрофона из списка"""
    global device, samplerate
    
    devices = sd.query_devices()
    input_devices = []
    
    print("\nДоступные микрофоны:")
    for i, dev in enumerate(devices):
        if dev['max_input_channels'] > 0:
            input_devices.append(i)
            print(f"{len(input_devices)}. {dev['name']} (Частота: {dev['default_samplerate']} Hz)")
    
    if not input_devices:
        print("Не найдено ни одного микрофона!")
        sys.exit(1)
    
    while True:
        try:
            choice = int(input("\nВыберите номер микрофона: ")) - 1
            if 0 <= choice < len(input_devices):
                device = input_devices[choice]
                device_info = sd.query_devices(device, 'input')
                samplerate = int(device_info['default_samplerate'])
                print(f"\nВыбрано устройство: {sd.query_devices(device)['name']}")
                print(f"Частота дискретизации: {samplerate} Hz")
                return
            print("Некорректный номер, попробуйте снова")
        except ValueError:
            print("Введите число!")

def is_valid_command(command: str) -> bool:
    """Проверяет, является ли команда значимой (не пустая и не только триггер)."""
    words = command.split()
    return any(word not in TRIGGERS for word in words)

def listen() -> str:
    """Слушает и возвращает распознанный текст."""
    def callback(indata, frames, time, status):
        Q.put(bytes(indata))

    with sd.RawInputStream(samplerate=samplerate, 
                         blocksize=16000, 
                         device=device,  # Исправлено здесь
                         dtype='int16', 
                         channels=1,
                         callback=callback):
        rec = KaldiRecognizer(vosk_model, samplerate)
        while True:
            data = Q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                return result.get("text", "").lower()

async def main():
    LUX_API.register(router)
    await LUX_API.say("Привет! я Люкс! ваш ассистент!")
    while True:
        print("Слушаем...")
        text = await asyncio.get_event_loop().run_in_executor(None, listen)

        if text and any(trigger in text for trigger in TRIGGERS):
            for trigger in TRIGGERS:
                text = text.replace(trigger, "").strip()

            if not is_valid_command(text):
                print("Только триггер. Жду полноценной команды.")
                continue

            command = recognize_command(text)
            if command:
                handler = router.try_run(command)
                if handler:
                    await handler(LUX_API, text)
                    print(f"Распознана команда: {command} - с текстом: {text}")
                else:
                    await LUX_API.say("Команда не распознана.")
            else:
                await LUX_API.say("Команда не распознана. Попробуйте сказать иначе.")
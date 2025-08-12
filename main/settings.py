import sys
import os
import importlib
import sounddevice as sd
from vosk import Model
from .config import PLUGINS_DIR, VOSK_MODEL_PATCH, SAMPLERATE, DEVICE

for filename in os.listdir(PLUGINS_DIR):
    if filename.endswith('.py') and filename != '__init__.py':
        module_name = filename[:-3]
        importlib.import_module(f'{PLUGINS_DIR}.{module_name}')
        

if not os.path.exists(VOSK_MODEL_PATCH):
    raise Exception(f"Модель Vosk не найдена по пути: {VOSK_MODEL_PATCH}")

vosk_model = Model(VOSK_MODEL_PATCH)

def select_microphone():
    """Функция для выбора микрофона из списка"""
    
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
                DEVICE = input_devices[choice]
                device_info = sd.query_devices(DEVICE, 'input')
                SAMPLERATE = int(device_info['default_samplerate'])
                print(f"\nВыбрано устройство: {sd.query_devices(DEVICE)['name']}")
                print(f"Частота дискретизации: {SAMPLERATE} Hz")
                return
            print("Некорректный номер, попробуйте снова")
        except ValueError:
            print("Введите число!")
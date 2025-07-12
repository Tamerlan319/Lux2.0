from pathlib import Path
import queue
from core.luxapi import Lux

LUX_API = Lux()

# Динамическая загрузка плагинов
PLUGINS_DIR = 'plugins'

# Настройки устройства и частоты
DEVICE = None
SAMPLERATE= 44100  # значение по умолчанию

Q = queue.Queue()

# Настройки Vosk
VOSK_MODEL_PATCH = str(Path(__file__).parent / "model")

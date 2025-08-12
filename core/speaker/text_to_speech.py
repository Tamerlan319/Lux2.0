import os
import torch
import soundfile as sf
import asyncio
import sounddevice as sd
from tempfile import NamedTemporaryFile
from core.config import MODEL_PATH, MODEL_URL

# Настройки TTS
device_torch = torch.device("cuda" if torch.cuda.is_available() else "cpu")
if not os.path.isfile(MODEL_PATH):
    torch.hub.download_url_to_file(MODEL_URL, MODEL_PATH)
model = torch.package.PackageImporter(MODEL_PATH).load_pickle("tts_models", "model")
model.to(device_torch)

torch.set_num_threads(4)
speaker = 'kseniya'
sample_rate = 48000

def sync_speak(text: str):
    # Генерация аудио
    audio = model.apply_tts(text=text, speaker=speaker, sample_rate=sample_rate)

    # Воспроизведение напрямую без записи на диск
    sd.play(audio, sample_rate)
    sd.wait()  # Ждём окончания, но это блокировка только для этого потока

async def speak(text: str):
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, sync_speak, text)

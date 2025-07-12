import os
import torch
import soundfile as sf
from tempfile import NamedTemporaryFile
import simpleaudio as sa
import asyncio
from core.config import MODEL_PATH, MODEL_URL

# Настройки TTS
device_torch = torch.device("cuda" if torch.cuda.is_available() else "cpu")
if not os.path.isfile(MODEL_PATH):
    torch.hub.download_url_to_file(MODEL_URL, MODEL_PATH)
model = torch.package.PackageImporter(MODEL_PATH).load_pickle("tts_models", "model")
model.to(device_torch)

torch.set_num_threads(4)
speaker = 'xenia'  # 'aidar', 'baya', 'kseniya', 'xenia', 'random'
sample_rate = 48000  # 8000, 24000, 48000

async def speak(text):
    # Генерация аудио
    audio = model.apply_tts(text=text, speaker=speaker, sample_rate=sample_rate)

    # Создание временного файла для хранения аудио
    with NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_file:
        sf.write(temp_audio_file.name, audio, sample_rate)
        temp_audio_file_path = temp_audio_file.name

    try:
        # Воспроизведение аудио через simpleaudio
        wave_obj = sa.WaveObject.from_wave_file(temp_audio_file_path)
        play_obj = wave_obj.play()
        await asyncio.sleep(0)  # Позволяет другим задачам выполняться
        play_obj.wait_done()  # Ждем окончания воспроизведения
    finally:
        # Удаление временного файла
        if os.path.exists(temp_audio_file_path):
            os.remove(temp_audio_file_path)

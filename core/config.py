from pathlib import Path

MODEL_DIR = Path(__file__).parent / "speaker"
MODEL_PATH = str(MODEL_DIR / "model.pt")
MODEL_URL = "https://models.silero.ai/models/tts/ru/ru_v3.pt"

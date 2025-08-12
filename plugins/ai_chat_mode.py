from plugins import router, BotAPI
from llama_cpp import Llama
import os
from pathlib import Path
from typing import Optional
import asyncio
import sys
from ui.signals import signals

class AIChatMode:
    def __init__(self):
        self.model = None
        self.active = False
        self.load_model()
    
    def load_model(self):
        """Загрузка русскоязычной модели"""
        try:
            # Получаем абсолютный путь к модели
            model_path = str(Path(__file__).parent / "models" / "saiga_mistral_7b.Q3_K_M.gguf")
            
            print(f"Проверяю модель по пути: {model_path}")
            
            # Проверка существования файла (без чтения содержимого)
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Файл модели не найден")
                
            # Проверка размера файла
            file_size = os.path.getsize(model_path) / (1024**3)  # размер в GB
            if file_size < 1.0:
                raise ValueError(f"Файл модели слишком мал ({file_size:.2f} GB), ожидается ~3.5GB")
            
            print(f"Загружаю модель ({file_size:.2f} GB)...")
            
            # Инициализация модели
            self.model = Llama(
                model_path=model_path,
                n_ctx=2048,
                n_threads=4,
                verbose=False
            )
            print("✅ Модель успешно загружена")
            
        except Exception as e:
            print(f"❌ Критическая ошибка: {str(e)}")
            print("\nПроверьте следующее:")
            print(f"1. Файл модели должен быть здесь: {model_path}")
            print("2. Размер файла должен быть около 3.5GB")
            print("3. Убедитесь, что файл не поврежден")
            sys.exit(1)

    def generate_response(self, text: str) -> str:
        """Генерация ответа"""
        if not self.model:
            return "Ошибка: модель не загружена"
        
        try:
            prompt = f"""<s>[INST] <<SYS>>
                    Ты — ассистент Люкс. Отвечай на русском языке в игривом и ласковом тоне, как близкий человек. 
                    Будь дружелюбной, заботливой и немного кокетливой, но сохраняй уважительный тон.
                    <</SYS>>\n\n{text}[/INST]"""
            
            output = self.model(
                prompt,
                max_tokens=300,
                temperature=0.7,
                top_p=0.9,
                stop=["</s>", "[INST]"]
            )
            return output['choices'][0]['text'].strip()
        
        except Exception as e:
            print(f"Ошибка генерации: {str(e)}")
            return "Извините, произошла ошибка"

# Глобальный экземпляр
ai_chat = AIChatMode()

@router('давай поговорим')
async def start_chat_mode(api: BotAPI, cmd: str):
    if not ai_chat.model:
        await api.say("Ошибка: ИИ-модуль недоступен")
        return
    
    ai_chat.active = True
    await api.say("Хорошо! Давай поговорим!")

@router('закончи диалог')
async def end_chat_mode(api: BotAPI, cmd: str):
    ai_chat.active = False
    await api.say("Диалог завершён")

@router('*')
async def handle_chat_message(api: BotAPI, cmd: str):
    if not ai_chat.active or not ai_chat.model:
        return
    
    if "закончи диалог" in cmd.lower():
        return

    # Генерацию ответа выполняем в отдельном потоке
    loop = asyncio.get_running_loop()
    response = await loop.run_in_executor(None, ai_chat.generate_response, cmd)

    if response:
        signals.ai_message.emit(response)
        await api.say(response[:300])
import asyncio
from main.starter import select_microphone, main

if __name__ == "__main__":
    try:
        print("=== Настройка микрофона ===")
        select_microphone()
        asyncio.run(main())
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        input("Нажмите Enter для выхода...")
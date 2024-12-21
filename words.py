TRIGGERS = {'люкс', 'lux', 'люксик'}

data_set = {
    # Анекдоты
    'расскажи анекдот': 'расскажи анекдот',
    'анекдот расскажи': 'расскажи анекдот',
    'хочу услышать анекдот': 'расскажи анекдот',
    'можешь рассказать анекдот?': 'расскажи анекдот',
    'расскажешь анекдот?': 'расскажи анекдот',
    'поведай анекдот': 'расскажи анекдот',
    'давай анекдот': 'расскажи анекдот',
    'есть анекдот?': 'расскажи анекдот',

    # Счёт
    'считай': 'считай',
    'начни считать': 'считай',
    'можешь начать считать?': 'считай',
    'рассчитай что-нибудь': 'считай',
    'запусти счёт': 'считай',
    'давай считать': 'считай',
    'посчитай': 'считай',
    'начни счёт': 'считай',

    # Остановка задач
    'останови счёт': 'останови счёт',
    'прекрати считать': 'останови счёт',
    'хватит считать': 'останови счёт',
    'останови всё': 'останови всё',
    'отмени задачи': 'останови всё',
    'заверши все задачи': 'останови всё',
    'хватит работать': 'останови всё',

    # Показ задач
    'покажи задачи': 'покажи задачи',
    'какие задачи запущены?': 'покажи задачи',
    'что сейчас работает?': 'покажи задачи',
    'список задач': 'покажи задачи',
    'активные задачи': 'покажи задачи',

    # Поиск в интернете
    'найди в интернете': 'найди в интернете',
    'поиск в интернете': 'найди в интернете',
    'ищи в интернете': 'найди в интернете',
    'поищи в интернете': 'найди в интернете',
    'помоги найти в интернете': 'найди в интернете',
    'покажи результаты поиска': 'найди в интернете',
    'что нашел в интернете': 'найди в интернете',
    'поищи что-нибудь в интернете': 'найди в интернете',

    # Открытие браузера
    'открой браузер': 'открой браузер',
    'запусти браузер': 'открой браузер',
    'открой интернет': 'открой браузер',
    'запусти интернет': 'открой браузер',
    'открой веб-браузер': 'открой браузер',
    'открой сайт': 'открой браузер',
}

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
import typing as t

# Обучение модели
vectorizer = CountVectorizer()
X_train = list(data_set.keys())
y_train = list(data_set.values())
X_vectorized = vectorizer.fit_transform(X_train)
classifier = LogisticRegression()
classifier.fit(X_vectorized, y_train)

def preprocess_command(command: str) -> str:
    """Удаляет лишние символы и нормализует текст команды."""
    import re
    command = command.lower()
    command = re.sub(r"[^\w\s]", "", command)
    command = re.sub(r"\s+", " ", command).strip()
    return command

def is_valid_command(command: str) -> bool:
    """Проверяет, является ли команда значимой (не пустая и не только триггер)."""
    words = command.split()
    return any(word not in TRIGGERS for word in words)

def recognize_command(command: str) -> t.Optional[str]:
    """Распознает команду с вероятностным порогом."""
    command = preprocess_command(command)

    # Проверка, чтобы команда содержала слова помимо триггеров
    if not is_valid_command(command):
        return None

    command_vectorized = vectorizer.transform([command])
    probabilities = classifier.predict_proba(command_vectorized)[0]
    max_prob_index = probabilities.argmax()
    max_prob = probabilities[max_prob_index]
    predicted_command = classifier.classes_[max_prob_index]

    # Увеличиваем порог вероятности
    threshold = 0.3
    if max_prob > threshold:
        return predicted_command
    return None

# Тестируем обработку команды
def process_command(input_text: str):
    """Обрабатывает текст команды."""
    # Проверяем наличие триггеров
    if not any(trigger in input_text.lower() for trigger in TRIGGERS):
        return "Триггер не найден, команда игнорируется."

    # Убираем триггер из текста команды
    for trigger in TRIGGERS:
        input_text = input_text.lower().replace(trigger, "").strip()

    # Распознаем команду
    recognized = recognize_command(input_text)
    if recognized:
        return f"Распознана команда: {recognized}"
    return "Команда не распознана."
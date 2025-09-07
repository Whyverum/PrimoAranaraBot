from random import choice

def get_best_response(user_text: str) -> str:
    """
    Подбирает наиболее подходящий ответ на сообщение пользователя.
    Сначала ищет ключевые слова и их синонимы, если совпадений нет — выдаёт случайную фразу.

    :param user_text: текст сообщения пользователя
    :return: строка с ответом
    """
    normalized_text: str = user_text.lower()

    for _, data in RESPONSES.items():
        for keyword in data["keywords"]:
            if keyword in normalized_text:
                return choice(data["answers"])

    return choice(RANDOM_PHRASES)

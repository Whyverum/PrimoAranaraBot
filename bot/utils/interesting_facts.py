from random import choice
from typing import Dict, List, Optional

from configs.config import Lists

__all__ = ("interesting_fact", "get_best_response",)

def interesting_fact(mode: str = "факт", lists: Optional[list[str]] = None) -> str:
    """
    Возвращает случайный факт, анекдот или цитату, в зависимости от режима.

    :param mode: строка, определяющая тип контента ("факт", "анекдот", "цитата").
    :param lists: необязательный список строк, из которого можно выбирать вручную.
    :return: случайный элемент из соответствующего списка.
    """
    if lists is not None:
        return choice(lists)

    mode = mode.lower()

    if mode == "анекдот":
        source: list[str] = Lists.jokes
    elif mode == "цитата":
        source: list[str] = Lists.quotes
    else:
        source: list[str] = Lists.facts

    return choice(source)


def get_best_response(
    user_text: str,
    responses: Dict[str, Dict[str, List[str]]],
    random_phrases: List[str],
) -> str:
    """
    Подбирает наиболее подходящий ответ на сообщение пользователя.
    Сначала ищет ключевые слова и их синонимы, если совпадений нет — выдаёт случайную фразу.

    :param user_text: текст сообщения пользователя
    :param responses: словарь с ключевыми словами и ответами
    :param random_phrases: список случайных фраз, если совпадений нет
    :return: строка с ответом
    """
    normalized_text: str = user_text.lower()

    # Перебор ключевых слов в словаре
    for _, data in responses.items():
        for keyword in data["keywords"]:
            if keyword in normalized_text:
                return choice(data["answers"])

    # Если совпадений нет — выдаём случайную фразу
    return choice(random_phrases)

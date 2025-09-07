from random import choice
from typing import List
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

router: Router = Router(name="reply_router")

RANDOM_PHRASES: List[str] = [
    "Бла-бла-бла!", "Хва-а-а-тит!", "Серьёзно? 😏", "Опять ты это говоришь...",
    "Хи-хи, смешно же!", "Ты снова шутник?", "Я уже слышал это раньше!", "Эй, не надо так!",
    "Ладно, ладно, хватит!", "Хмм... интересно...", "Ты меня удивляешь!", "А давай лучше что-то новое?",
    "Не могу поверить!", "Ахаха, это забавно!", "Серьёзно? Ну ладно...", "Эй, это уже слишком!",
    "О, это было неожиданно!",
]


@router.message()
async def reply_message(message: Message, state: FSMContext) -> None:
    # Достаём данные из состояния
    data = await state.get_data()
    last_bot_text = data.get("last_bot_text", "")

    # КРИТИЧЕСКИ ВАЖНО: Проверяем, что состояние не пустое после перезапуска.
    # Если состояние пустое (например, после перезапуска), то мы НЕ должны считать,
    if last_bot_text and message.text and message.text.strip() == last_bot_text.strip():
        response = "Не повторяй за мной!"
    else:
        response = choice(RANDOM_PHRASES)

    ids = message.message_id-1
    print(str())

    # Отправляем ответ и ПОЛУЧАЕМ ОБЪЕКТ ОТПРАВЛЕННОГО СООБЩЕНИЯ
    sent_message = await message.reply(response)

    # Сохраняем текст последнего сообщения бота в состоянии
    # Теперь состояние будет обновлено после каждого сообщения бота
    await state.update_data(last_bot_text=sent_message.text)
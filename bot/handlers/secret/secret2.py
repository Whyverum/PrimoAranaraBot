from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

# Создаем роутер
knowledge_router = Router()


# Определяем состояния
class KnowledgeStates(StatesGroup):
    question1 = State()
    question2 = State()
    question3 = State()
    question4 = State()
    question5 = State()
    question6 = State()


# Вопросы и ответы (замените на свои)
QUESTIONS = {
    1: "Вопрос1",
    2: "Вопрос2",
    3: "Вопрос3",
    4: "Вопрос4",
    5: "Вопрос5",
    6: "Вопрос6"
}

ANSWERS = {
    1: {"Ответ 11": "СообщениеА1", "Ответ 12": "СообщениеБ1"},
    2: {"Ответ 21": "СообщениеА2", "Ответ 22": "СообщениеБ2"},
    3: {"Ответ 31": "СообщениеА3", "Ответ 32": "СообщениеБ3"},
    4: {"Ответ 41": "СообщениеА4", "Ответ 42": "СообщениеБ4"},
    5: {"Ответ 51": "СообщениеА5", "Ответ 52": "СообщениеБ5"},
    6: {"Ответ 61": "СообщениеА6", "Ответ 62": "СообщениеБ6"}
}

FINAL_MESSAGES = {
    "all_1": "ИТОГ1 - Все ответы первого типа!",
    "all_2": "ИТОГ2 - Все ответы второго типа!",
    "mixed": "ИТОГ1 - Смешанные ответы!"
}


# Запуск сессии знаний
@knowledge_router.message(StateFilter(None), Command("знания"))
@knowledge_router.message(StateFilter(None), F.text.casefold() == "пора заняться знаниями")
async def start_knowledge_session(message: Message, state: FSMContext):
    await message.answer("Отлично! Начинаем сессию знаний! 🧠")
    await message.answer(QUESTIONS[1])
    await state.set_state(KnowledgeStates.question1)
    await state.update_data(answers={})


# Обработчики для каждого вопроса
@knowledge_router.message(KnowledgeStates.question1, F.text.in_(ANSWERS[1].keys()))
async def process_question1(message: Message, state: FSMContext):
    user_answer = message.text
    response_message = ANSWERS[1][user_answer]

    # Сохраняем ответ
    answer_code = 1 if user_answer == "Ответ 11" else 2
    await state.update_data(answers={"q1": answer_code})

    # Отправляем сообщение и следующий вопрос
    await message.answer(response_message + "\n\n" + QUESTIONS[2])
    await state.set_state(KnowledgeStates.question2)


@knowledge_router.message(KnowledgeStates.question2, F.text.in_(ANSWERS[2].keys()))
async def process_question2(message: Message, state: FSMContext):
    user_answer = message.text
    response_message = ANSWERS[2][user_answer]

    # Сохраняем ответ
    answer_code = 1 if user_answer == "Ответ 21" else 2
    data = await state.get_data()
    answers = data.get("answers", {})
    answers["q2"] = answer_code
    await state.update_data(answers=answers)

    # Отправляем сообщение и следующий вопрос
    await message.answer(response_message + "\n\n" + QUESTIONS[3])
    await state.set_state(KnowledgeStates.question3)


# Добавьте аналогичные обработчики для question3-question5

@knowledge_router.message(KnowledgeStates.question6, F.text.in_(ANSWERS[6].keys()))
async def process_question6(message: Message, state: FSMContext):
    user_answer = message.text
    response_message = ANSWERS[6][user_answer]

    # Сохраняем ответ
    answer_code = 1 if user_answer == "Ответ 61" else 2
    data = await state.get_data()
    answers = data.get("answers", {})
    answers["q6"] = answer_code
    await state.update_data(answers=answers)

    # Отправляем финальное сообщение
    await message.answer(response_message)
    await finish_knowledge_session(message, state)


# Обработчики для некорректных ответов
@knowledge_router.message(KnowledgeStates.question1)
async def process_incorrect_answer1(message: Message):
    await message.answer("Пожалуйста, выберите один из предложенных вариантов ответа.")
    await message.answer(QUESTIONS[1])


@knowledge_router.message(KnowledgeStates.question2)
async def process_incorrect_answer2(message: Message):
    await message.answer("Пожалуйста, выберите один из предложенных вариантов ответа.")
    await message.answer(QUESTIONS[2])


# Добавьте аналогичные обработчики для остальных вопросов

# Завершение сессии
async def finish_knowledge_session(message: Message, state: FSMContext):
    data = await state.get_data()
    answers = data.get("answers", {})

    # Проверяем результаты
    if all(answer == 2 for answer in answers.values()):
        await message.answer(FINAL_MESSAGES["all_2"])
    else:
        await message.answer(FINAL_MESSAGES["mixed"])

    await state.clear()

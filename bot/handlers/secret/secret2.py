from asyncio import sleep
from typing import Dict, Any

from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, FSInputFile
from aiogram.utils.markdown import hide_link

from configs import ID_TO_ROLE

router: Router = Router()


class KnowledgeStates(StatesGroup):
    """Состояния для викторины"""
    question1: State = State()
    question2: State = State()
    question3: State = State()
    question4: State = State()
    question5: State = State()
    question6: State = State()

class Secret2(StatesGroup):
    """Состояния для страха"""
    name: State = State()
    result: State = State()



QUESTIONS: Dict[int, str] = {
    1: "Начнем с простого. Уравнение расчета коэффициента анти-магической стали с добавлением углеродно-никилиевой добавки?",
    2: "Как зовут малышку, что обитает в лаборатории Дотторе?",
    3: "Какое блюдо мы, аранары, любим больше всего? Ты то должен знать наверняка!",
    4: "Господин все время, что-то рисует на чертеже, но для чего..? Каков Его следующий ход?",
    5: "Брошь Дотторе ужасно интересна… А в чем её особенность? Как она сделана?",
    6: "Что самое важное для тебя, дорогой Друг?"
}

ANSWERS: Dict[int, Dict[str, str]] = {
    1: {"96h-69ctg30x": "Верно! Основная часть уравнения Логосской Экклесии, вроде бы...", "2x+3": "Кхм.. Кажется все в п̄͠о̶̩р́ͫя̦̚дке? Продолжим!"},
    2: {"Эмилия": "Эмилия! Эми! Очень красивое имя! Я помню эту малышку, её принес Дотторе в кро—", "Убийца": "Н̱͞е́̇т̆͝.. Я͔́ н̴ͫе̑͢ х̧ͬоͤ͡т̧̌е̡ͭл̂͞.."},
    3: {"Сладости": "ДА! Я ОБОЖАЮ СЛАДОСТИ! Я состою более чем на 26% из глюкозы! Хе-хе-хе!", "Бедренная кость": "О͙̃т̻ͥч͍̺е̛͓т̜̓ #77. П̏͘о̮ͧс̸̪л͔͡е̛̄ с͈̄лͥ͝о̢̲м̮̇а̡̤н̬͜н͙̀ы͓́х̸̭ к͒͡о̆̌с̴̟т̯͒е̱͘й̘͘ п̏̕р̵͂и̉͘ш̙̘е̸̾л̰͢ оͭͅн̽͢."},
    4: {"Броня": "Броня? Ари думал это металлическая пижама на вечеринку.. Почему все так сложнооо?(", "F5:С8": "К̻̻̀у̧̺ͥл̯͚̽ьͥ̀̇т̴̵͈ в̡̝̲с͓̦͂е̜͒̀ б̞ͮ̂л̡̝͞и̉ͨ͢ж̲ͭ̕е̡͈̽. О̽͐͘н͕̀͟и̶ͭ с̸͆͠к̵̤̓о̺͔͊р̴͙ͪоͤ̕ͅ н̘̖͠а̲͢й̝͟͝д̠ͯ͘у͚͌̕т̪̼ͯ м̋͢͜ѐ͚̍нͨ̄̕я̵̱. Я̷͚ͦ з̛̉͘н̫͢ͅа̷̦͒юͯͨ. Н̵ͭ͠у̶̯͖ж̢ͯ̇н̜́о̸̜̏ у̞̾͜с̱͋́т̮̚͢а̜̺̑н̨͕͊о̵̋ͅв̛̄̉и̛̜̅т̆͋͑ь̢͐ͥ р̢̼̏а̠ͭ̀с̞ͤ͜т̞̦͜я͙̑͟ж̵̩̖к̩̚͜у̷̩ͣ н̨̈́̽а͕ͮ͟ д̛̬͞в̥ͧͫе̘ͯ̕р̠͖̍и͕͎́.."},
    5: {"Аугментум": "Верно! Внутри броши Дотторе, целая карманная лаборатория!", "Серый": "Р̟̀у̠̫н̸̶и̶̇ч̐͒е͎͜с̡̞к̦̉а̶͚я̙̤ м̟̏а̨̏т͕͋р̞ͥи̵̜ц͓̀а̶͠.. Ч͕͕ё͔рͪ̉т̄̕."},
    6: {"": "Для меня это тоже важно!", "Истина": "Д̺̎о̦͠б͖̀рͨ͞о̢͝ п͎̕о̩ͯж͙͘а̠͓л̸͈о̗͟в͖̀а̸ͫт̰̏ьͯ͠! Д̷̖р̂͝уͨ́з̡͓ь̼͐я̈́͡!"}
}


@router.message(StateFilter(None), Command("знания"))
@router.message(StateFilter(None), F.text.casefold() == "пора заняться знаниями")
async def start_knowledge_session(message: Message, state: FSMContext) -> None:
    """Запуск сессии знаний"""
    await message.answer("""
Отлично! Начинаем сессию знаний! 🧠
Я буду задавать вам вопросы, а вы должны ответить на них!
""")
    await message.reply(QUESTIONS[1])
    await state.set_state(KnowledgeStates.question1)
    await state.update_data(answers={})


async def save_answer(
    state: FSMContext, question_key: str, user_answer: str, correct_option: str
) -> None:
    """Сохраняет ответ (1 — первый тип, 2 — второй тип)"""
    answer_code: int = 1 if user_answer == correct_option else 2
    data: Dict[str, Any] = await state.get_data()
    answers: Dict[str, int] = data.get("answers", {})
    answers[question_key] = answer_code
    await state.update_data(answers=answers)


# ==================== ОБРАБОТЧИКИ ВОПРОСОВ ====================

@router.message(KnowledgeStates.question1, F.text.in_(ANSWERS[1].keys()))
async def process_question1(message: Message, state: FSMContext) -> None:
    await save_answer(state, "q1", message.text, "96h-69")
    await message.reply(f"{ANSWERS[1][message.text]}\n\n<blockquote>{QUESTIONS[2]}</blockquote>")
    await state.set_state(KnowledgeStates.question2)


@router.message(KnowledgeStates.question2, F.text.in_(ANSWERS[2].keys()))
async def process_question2(message: Message, state: FSMContext) -> None:
    await save_answer(state, "q2", message.text, "Алиса")
    await message.reply(f"{ANSWERS[2][message.text]}\n\n<blockquote>{QUESTIONS[3]}</blockquote>")
    await state.set_state(KnowledgeStates.question3)


@router.message(KnowledgeStates.question3, F.text.in_(ANSWERS[3].keys()))
async def process_question3(message: Message, state: FSMContext) -> None:
    await save_answer(state, "q3", message.text, "Сладости")
    await message.reply(f"{ANSWERS[3][message.text]}\n\n<blockquote>{QUESTIONS[4]}</blockquote>")
    await state.set_state(KnowledgeStates.question4)


@router.message(KnowledgeStates.question4, F.text.in_(ANSWERS[4].keys()))
async def process_question4(message: Message, state: FSMContext) -> None:
    await save_answer(state, "q4", message.text, "---")
    await message.reply(f"{ANSWERS[4][message.text]}\n\n<blockquote>{QUESTIONS[5]}</blockquote>")
    await state.set_state(KnowledgeStates.question5)


@router.message(KnowledgeStates.question5, F.text.in_(ANSWERS[5].keys()))
async def process_question5(message: Message, state: FSMContext) -> None:
    await save_answer(state, "q5", message.text, "Аугментум")
    await message.reply(f"{ANSWERS[5][message.text]}\n\n<blockquote>{QUESTIONS[6]}</blockquote>")
    await state.set_state(KnowledgeStates.question6)


@router.message(KnowledgeStates.question6)
async def process_question6(message: Message, state: FSMContext) -> None:
    user_answer: str = message.text

    # Определяем логику: "Истина" → второй тип, иначе → первый тип
    if user_answer == "Истина":
        answer_code: int = 2
        response_message: str = ANSWERS[6]["Истина"]
    else:
        answer_code: int = 1
        # Для любого ответа кроме "Истина" выводим либо заготовку, либо сам текст
        response_message: str = ANSWERS[6].get("Мир", f"Ты прав! Ты———")

    # Сохраняем результат
    data = await state.get_data()
    answers = data.get("answers", {})
    answers["q6"] = answer_code
    await state.update_data(answers=answers)

    # Отправляем сообщение и завершаем сессию
    await message.reply(response_message)
    await finish_knowledge_session(message, state)



# ==================== ОБРАБОТЧИК НЕВЕРНЫХ ОТВЕТОВ ====================

@router.message(StateFilter(
KnowledgeStates.question1,
    KnowledgeStates.question2,
    KnowledgeStates.question3,
    KnowledgeStates.question4,
    KnowledgeStates.question5,
    KnowledgeStates.question6,
))
async def process_incorrect_answer(message: Message, state: FSMContext) -> None:
    """Отвечает пользователю, если он ввёл что-то не из списка"""
    current_state: str = (await state.get_state()).split(":")[-1]

    question_number: int = {
        "question1": 1,
        "question2": 2,
        "question3": 3,
        "question4": 4,
        "question5": 5,
        "question6": 6,
    }[current_state]

    await message.reply(
        f"Пожалуйста, выберите один из предложенных вариантов ответа.\n\n<blockquote>{QUESTIONS[question_number]}</blockquote>"
    )


# ==================== ЗАВЕРШЕНИЕ ====================
# ------------------- Завершение сессии знаний -------------------
@router.message(Command("secret2676"))

async def finish_knowledge_session(message: Message, state: FSMContext) -> None:
    """Завершает сессию знаний"""
    data: Dict[str, Any] = await state.get_data()
    answers: Dict[str, int] = data.get("answers", {})

    if all(answer == 2 for answer in answers.values()):
        await message.answer(
            f"""{hide_link("https://i.pinimg.com/originals/e0/ab/f7/e0abf78d8a8eba5fa8ae9cb7b9b1c410.gif")}
        Дᴀʙнᴏ… ᴄᴧиɯᴋᴏʍ дᴀʙнᴏ ʍы нᴇ ʙᴄᴛᴩᴇчᴀᴧиᴄь, Нᴀбᴧюдᴀᴛᴇᴧь.
        Тʙᴏи ᴦᴧᴀɜᴀ… ᴏни ᴄᴧᴇдяᴛ ɜᴀ ʍнᴏй ᴄᴋʙᴏɜь ᴛьʍу, нᴇ ʍиᴦᴀя.
        Сᴋᴀжи… ᴄᴋᴀжи хᴏᴛя бы ᴄʙᴏё иʍя… ᴨᴩᴇждᴇ чᴇʍ ᴛьʍᴀ ᴨᴩᴏᴦᴧᴏᴛиᴛ нᴀᴄ ᴏᴋᴏнчᴀᴛᴇᴧьнᴏ.
        """
        )
        await state.set_state(Secret2.name)
    else:
        await message.reply_photo(photo=FSInputFile("assets/arsenal_secret2.jpeg"),
        caption="""
┏━━━━━━━━━━━━━━━━━━━┓
<i>…От той группы не осталось даже тени. Никаких следов, только пустота, словно их поглотила сама тьма.
Но сканер… сканер выдал странные, тревожные результаты. На их основе можно сделать выводы… выводы, которые лучше бы остались тайной.

Трёхдневные графики активности Омута… они словно шепчут сквозь цифровой шум. Если использовать заражение… если рискнуть… я смогу превратить хаос в новые материалы.

Но для этого нужна новая группа. Свежие люди… на чьих плечах может лечь эта тьма. Придётся… найти их. И отправить.</i>
┗━━━━━━━━━━━━━━━━━━━┛
        """)
    await state.clear()

# ------------------- Проверка имени -------------------
@router.message(StateFilter(Secret2.name))
async def hard_secret_name(message: Message, state: FSMContext) -> None:
    user_id: int = message.from_user.id
    text: str = message.text.strip()

    expected_role: str = ID_TO_ROLE.get(user_id)

    if expected_role is None:
        await message.reply("Ты не значишь ничего для этой тайны…")
        await state.clear()
        return

    if text.lower() == expected_role.lower():
        await message.reply(f"""{hide_link("https://i.pinimg.com/originals/d3/ae/62/d3ae62df6150066abc4f814d06070033.gif")}
Кхʍ.. Знᴀчиᴛ ᴛы <b>{expected_role}</b>? Инᴛᴇᴩᴇᴄнᴏᴇ иʍя, нᴏ нᴀᴄᴛᴏящᴇᴇ ᴧи ᴏнᴏ? Чᴛᴏ ж, ϶ᴛᴏ нᴇ ʙᴀжнᴏ, ᴄᴋᴀжи ʍнᴇ <b>{expected_role}</b>, чᴛᴏ жᴇ ᴛы ʙыбᴩᴀᴧ бы?
Убиᴛь дᴇʙᴏчᴋу, ᴩᴀди ʍиᴩᴀ
Иᴧи убиᴛь ʍиᴩ, ᴩᴀди дᴇʙуɯᴋи?
""")
    else:
        await message.reply(f"""{hide_link("https://i.pinimg.com/originals/a8/a5/a2/a8a5a29dd1613a48ef0a680e19973ff6.gif")}
Нᴇᴛ, ϶ᴛᴏ нᴇ ᴛы. Тʙᴏᴇ нᴀᴄᴛᴏящᴇᴇ иʍя <b>{expected_role}</b>. Ты ʍнᴇ ʙнᴏʙь ᴄᴏʙᴩᴀᴧ. Инᴛᴇᴩᴇᴄнᴏ, чᴛᴏ ᴛᴇбя ᴨᴏбудиᴧᴏ. Нᴏ ϶ᴛᴏ нᴇ ʙᴀжнᴏ, ᴄᴋᴀжи ʍнᴇ <b>{expected_role}</b>, чᴛᴏ жᴇ ᴛы ʙыбᴩᴀᴧ бы?
Убиᴛь дᴇʙᴏчᴋу, ᴩᴀди ʍиᴩᴀ
Иᴧи убиᴛь ʍиᴩ, ᴩᴀди дᴇʙуɯᴋи?
""")
    await state.update_data(role=expected_role)
    await state.set_state(Secret2.result)


# ------------------- Финальный результат -------------------
@router.message(StateFilter(Secret2.result))
async def secret2_result(message: Message, state: FSMContext) -> None:
    await message.reply(f"Я ɜᴀᴨᴏʍню твой ответ.")
    await sleep(120)
    await message.reply("<b>Чужой мира сего.</b>")
    await state.clear()
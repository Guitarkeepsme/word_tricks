from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import games_code
from time import monotonic

t = monotonic()
API_TOKEN = '6070755171:AAFzOBUDrYpsvFNncZULkPA74FkWuB8PT4I'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


class Forms(StatesGroup):
    start = State()
    back = State()
    from_big = State()
    find_small = State()
    words_sequence = State()
    playing_words_sequence = State()


commands = ["Из большого слова маленькие", "Маленькое слово внутри больших", "Вернуться", "Игра в слова"]


@dp.message_handler(Text(equals="Вернуться"), state='*')
async def go_back(message: types.Message):
    buttons = ["Из большого слова маленькие", "Маленькое слово внутри больших", "Игра в слова", "Вернуться"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    await Forms.start.set()
    keyboard.add(*buttons)
    await message.reply("Что ж, начнём заново. \n\nВыбери игру!", reply_markup=keyboard)


@dp.message_handler(commands="start", state="*")
async def send_welcome(message: types.Message):
    buttons = ["Из большого слова маленькие", "Маленькое слово внутри больших", "Игра в слова"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    keyboard.add(*buttons)
    await Forms.start.set()
    await message.reply("Привет, " + "*" + message.from_user.first_name +
                        "*! 👋 \n\nЯ буду помогать тебе искать слова. ""\nВыбери игру!", reply_markup=keyboard,
                        parse_mode='Markdown')


@dp.message_handler(Text(equals="Из большого слова маленькие"), state=Forms.start)
async def from_big(message: types.Message):
    buttons = ["Вернуться"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    keyboard.add(*buttons)
    await message.reply("Введи слово, из которого ты хочешь получить список маленьких слов.", reply_markup=keyboard)
    await Forms.from_big.set()


@dp.message_handler(state=Forms.from_big)
async def from_big_search(message: types.Message):
    button = ["Вернуться"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    keyboard.add(*button)
    answer = games_code.from_big(message.text, games_code.final_result)
    if message.text == "Вернуться":
        await Forms.start.set()
        await go_back
    elif message.text.lower() not in games_code.final_result:
        await message.reply("Не знаю такого слова. Напиши другое.",
                            reply_markup=keyboard, parse_mode="Markdown")
    else:
        await message.reply("Из этого слова можно составить такие слова: \n\n*" +
                            ', '.join(answer) + "*" + "\n\n Количество слов: *" + str(len(answer)) + "*",
                            parse_mode="Markdown", reply_markup=keyboard)


@dp.message_handler(Text(equals="Маленькое слово внутри больших"), state=Forms.start)
async def find_small(message: types.Message):
    buttons = ["Вернуться"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    keyboard.add(*buttons)
    await message.reply("Введи слово, которое ты хочешь найти в других словах.\n\n\n Обрати внимание, "
                        "что я могу вывести не более 200 слов, но каждый раз разных.", reply_markup=keyboard)
    await Forms.find_small.set()


@dp.message_handler(lambda message: message.text not in commands, state=Forms.start)
async def invalid_message(message: types.Message):
    return await message.reply("Не понимаю, о чём ты. Проверь, верно ли ты ввёл команду.")


@dp.message_handler(state=Forms.find_small)
async def find_small_search(message: types.Message):
    button = ["Вернуться"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    keyboard.add(*button)
    answer = games_code.find_small(message.text, games_code.final_result)
    if message.text == "Вернуться":
        await Forms.start.set()
        await go_back
    else:
        await message.reply("Это слово есть внутри таких слов: \n\n*" +
                            ', '.join(answer) + "*" + "\n\n Количество слов: *" + str(len(answer)) + "*",
                            parse_mode="Markdown", reply_markup=keyboard)


@dp.message_handler(Text(equals="Игра в слова"), state=Forms.start)
async def words_sequence(message: types.Message):
    buttons = ["Вернуться"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    keyboard.add(*buttons)
    if message.text == "Вернуться":
        await Forms.start.set()
        await go_back
    else:
        await Forms.words_sequence.set()
        await message.reply("Давай напомню правила: \n\nТы называешь слово *(существительное, не название)*, "
                            "а я в ответ пишу слово, первая буква которого совпадает с последней буквой твоего слова. "
                            "Затем ты делаешь то же самое. \nЕсли названо слово, заканчивающееся на Й, Ы, Ъ, Ь, "
                            "следущему игроку нужно придумать слово на *предпоследнюю* букву. "
                            "Слова в процессе одного кона игры не должны повторяться.\n\n\n" +
                            "А теперь введи начальное слово.", parse_mode="Markdown", reply_markup=keyboard)


@dp.message_handler(state=Forms.words_sequence)
async def words_sequence(message: types.Message, state: FSMContext):
    button = ["Вернуться"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    keyboard.add(*button)
    global used_words
    used_words = [message.text]
    answer = games_code.words_sequence(message.text, games_code.final_result, used_words)
    used_words.append(answer)
    if message.text == "Вернуться":
        await Forms.start.set()
        await go_back
    if message.text.lower() not in games_code.final_result:
        await message.reply("Не знаю такого слова. Напиши другое.",
                            reply_markup=keyboard, parse_mode="Markdown")
    else:
        if answer[-1] in games_code.banned_letters:
            answer_cut = answer[:-1]
            async with state.proxy() as current_word:
                current_word['word'] = answer_cut
        else:
            async with state.proxy() as current_word:
                current_word['word'] = answer
        await message.reply("*" + answer + "*", parse_mode="Markdown", reply_markup=keyboard)
        await Forms.playing_words_sequence.set()


@dp.message_handler(lambda message: message.text.lower(), state=Forms.playing_words_sequence)
async def playing_words_sequence(message: types.Message, state: FSMContext):
    button = ["Вернуться"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    keyboard.add(*button)
    if message.text == "Вернуться":
        await Forms.start.set()
        await go_back
    if message.text.lower() not in games_code.final_result:
        await message.reply("Не знаю такого слова. Напиши другое.",
                            reply_markup=keyboard, parse_mode="Markdown")
    elif message.text.lower() in used_words:
        await message.reply("Это уже было. Напиши другое слово.",
                            reply_markup=keyboard, parse_mode="Markdown")
    else:
        check_word = await state.get_data()
        if check_word['word'][-1] != message.text.lower()[0]:
            await message.reply("Это слово не подходит! Напиши слово на букву *" + str(check_word['word'][-1]) + "*",
                                reply_markup=keyboard, parse_mode="Markdown")
        else:
            await Forms.words_sequence.set()
            await state.update_data(word=check_word['word'])
            answer = games_code.words_sequence(message.text, games_code.final_result, used_words)
            used_words.append(answer)

            if message.text == "Вернуться":
                await Forms.start.set()
                await go_back
            else:
                if answer[-1] in games_code.banned_letters:
                    answer_cut = answer[:-1]
                    async with state.proxy() as current_word:
                        current_word['word'] = answer_cut
                else:
                    async with state.proxy() as current_word:
                        current_word['word'] = answer
                await message.reply("*" + answer + "*", parse_mode="Markdown", reply_markup=keyboard)
                # start_timer = 30
                # timer_message = await bot.send_message(chat_id=message.chat.id, text=f"Осталось {start_timer} секунд")
                # zero_timer_check = 0
                # for seconds_left in range(start_timer - 1, -1, -1):
                #     await asyncio.sleep(1)
                #     await timer_message.edit_text(f"Осталось *{seconds_left}* секунд", parse_mode="Markdown")
                #     if seconds_left == 0:
                #         zero_timer_check += 1
                # if zero_timer_check == 1:
                #     await bot.send_message(chat_id=message.chat.id, text="Время вышло. "
                #                            "*Вы проиграли!*", parse_mode="Markdown", reply_markup=keyboard)
                if len(answer) == 0:
                    await bot.send_message(chat_id=message.chat.id, text="Я не могу найти ни одного подходящего слова, "
                                                                         "а это значит, что вы победили.\n\n\n"
                                           "*Поздравляю!*", parse_mode="Markdown", reply_markup=keyboard)
                used_words.append(answer)
                used_words.append(message.text)
                await Forms.playing_words_sequence.set()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

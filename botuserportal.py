from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps
from pyowm.utils.config import get_default_config
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import ChatType

#класс
class MyBot:
    #инициализация бота
    def __init__(self):
        self._TOKEN = '5689385764:AAFs8vZoZGrSYUN-kqkDifoj0I0lEZh1dnU'#токен
        self.bot = Bot(self._TOKEN)
        self.dp = Dispatcher(bot=self.bot, storage=MemoryStorage())
        self.memory = MemoryStorage()

    def start(self):
        #элементы клавиатуры
        help_button = KeyboardButton('/help 🎫')
        price_button = KeyboardButton('/price 📠')
        info_button = KeyboardButton('/info 📊')
        pay_button = KeyboardButton('/reg 💵')
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(help_button, price_button, info_button, pay_button)
        #команды
        @self.dp.message_handler(commands=['start'])
        async def hello(message: types.message):
            await message.answer('привет наши /help что бы узнать список команд')

        @self.dp.message_handler(commands=['help'])
        async def hello(message: types.message):
            await message.answer('что умее этот бот???\n/price - цены и информация о занят  иях и группе\n/info - о нас \n/pay - оплата', reply_markup=keyboard)

        @self.dp.message_handler(commands=['price'])
        async def hello(message: types.message):
            await message.answer('nothing...', reply_markup=keyboard)

        @self.dp.message_handler(commands=['info'])
        async def hello(message: types.message):
            await message.answer('nothing...', reply_markup=keyboard)
        #регистрация
        @self.dp.message_handler(commands=['reg'])
        async def registration_handler(msg: types.Message):
            # Отправляем первый вопрос
            await msg.answer("Как вас зовут?")
            
            # Ожидаем ответ
            answer_1 = await bot.await_answer()
            name = answer_1.text
            
            # Отправляем второй воп
            await msg.answer("Сколько вам лет?")
            
            # Ожидаем ответ
            answer_2 = await bot.await_answer()
            age = answer_2.text
            
            #... добавляем другие вопросы ияем ответы
            
            # Выводим результат опроса
            result_message = f"Спасибо за регистрацию, {name}! Ваш возраст {age}."
            await msg.answer(result_message)

#запуск сервера
        executor.start_polling(self.dp, skip_updates=True)
#старт сервера
if __name__ == '__main__':
    bot = MyBot()
    bot.start()
#examle
'''
        @self.dp.message_handler(commands=['reg'])
        async def hello(msg: types.Message):
                mes = msg.text

                if mes == 'Привет':
                    await self.dp.bot.send_message(chat_id=msg.from_user.id, text="Привет тебе тоже!")
'''
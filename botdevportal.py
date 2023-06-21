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
        self._TOKEN = '5759536990:AAGisVBTSrScFeECXF-0mq6MuenGAuxEPuo'#токен
        self.bot = Bot(self._TOKEN)
        self.dp = Dispatcher(bot=self.bot, storage=MemoryStorage())
        self.memory = MemoryStorage()

    def start(self):
        #элементы клавиатуры
        help_button = KeyboardButton('/help 🎫')
        price_button = KeyboardButton('/showdb ')
        info_button = KeyboardButton('/statistics 📊')
        pay_button = KeyboardButton('/sending ')
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(help_button, price_button, info_button, pay_button)
        #команды
        @self.dp.message_handler(commands=['start'])
        async def hello(message: types.message):
            await message.answer('привет наши /help что бы узнать список команд')

        @self.dp.message_handler(commands=['help'])
        async def hello(message: types.message):
            await message.answer('что умее этот бот???\n/price - цены и информация о занят  иях и группе\n/info - о нас \n/pay - оплата', reply_markup=keyboard)

        @self.dp.message_handler(commands=['/showdb'])
        async def hello(message: types.message):
            await message.answer('nothing...', reply_markup=keyboard)

        @self.dp.message_handler(commands=['statistics'])
        async def hello(message: types.message):
            await message.answer('nothing...', reply_markup=keyboard)

        @self.dp.message_handler(commands=['sending'])
        async def hello(message: types.message):
            await message.answer('nothing...', reply_markup=keyboard)
#запуск сервера
        executor.start_polling(self.dp, skip_updates=True)
#старт сервера
if __name__ == '__main__':
    bot = MyBot()
    bot.start()
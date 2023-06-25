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
import sqlite3
from aiogram import *
import time
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
        price_button = KeyboardButton('/showusersdb 📜')
        info_button = KeyboardButton('/statistics 📊')
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(help_button, price_button, info_button)
        #команды
        @self.dp.message_handler(commands=['start'])
        async def hello(message: types.message):
            await message.answer('привет напиши /help что бы узнать список команд')

        @self.dp.message_handler(commands=['help'])
        async def hello(message: types.message):
            await message.answer('🎫что умеет этот бот???🎫\n/showusersdb - покацавет информацию о зарегестрированных пользователях\n/statistics - количевство зарегестрированных позьлователей \n/sending - рассылка пользователям телеграмм канала', reply_markup=keyboard)

        @self.dp.message_handler(commands=['showusersdb'])
        async def hello(message: types.message):
            # Создание подключения к базе данных
            await message.answer('📜пожалуйста подождите идет обработка данных📜')
            print("была показанна база данных время :",time.ctime())
                # Создание подключения к базе данных
            conn = sqlite3.connect('users.db')
            cur = conn.cursor()
            # Выполнение запроса к базе данных
            cur.execute("SELECT * FROM users")
            # Чтение результатов запроса
            rows = cur.fetchall()
            # Вывод результатов в консоль
            for row in rows:
                await message.answer(row)
            print("была успешно выведены база данных время :",time.ctime())
            # Закрытие подключения к базе данных
            conn.close()
            print('завершено соединения с базой данных время :',time.ctime())

        @self.dp.message_handler(commands=['statistics'])
        async def hello(message: types.message):
                # Создание подключения к базе данных
            conn = sqlite3.connect('users.db')
            cur = conn.cursor()

            # Выполнение запроса к базе данных
            cur.execute("SELECT numberid FROM users ORDER BY ROWID DESC LIMIT 1")

            # Получение результата запроса
            result = cur.fetchone()[0]

            # Вывод результата в коноль
            await message.answer(f"📊есть {result} пользователей записанных на ваше мероприятие📊")

            # Закрытие подключения к базе данных
            conn.close()

        @self.dp.message_handler(commands=['sending'])
        async def hello(message: types.message):
            mes = message.text
            mes = mes.replace("/sending📨","")
            mes = mes.replace("/sending","")
            await message.answer('📨старт рассылки📨', reply_markup=keyboard)
            await self.dp.bot.send_message(chat_id='1001989620505', text=mes)#1001989620505    
            print('начан старт рассылки по id 1001989620505 время :',time.ctime())
            
#запуск сервера
        executor.start_polling(self.dp, skip_updates=True)
#старт сервера
if __name__ == '__main__':
    bot = MyBot()
    bot.start()
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
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.types.reply_keyboard import ReplyKeyboardRemove
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from aiogram import types
import sqlite3
import time 

conn = sqlite3.connect('users.db')

# Создаем таблицу для хранения информации о пользователях
conn.execute('''CREATE TABLE IF NOT EXISTS users
             (numberid INTEGER PRIMARY KEY AUTOINCREMENT,
             username TEXT,
             usersurname TEXT,
             course TEXT,
             userage TEXT,
             pay TEXT,
             contactnumbern TEXT
             )''')

#класс
class MyBot(FSMContext,StatesGroup): 
    # Создаем именованные состояния (states) для каждой стадии опроса
    ENTER_NAME = State()
    ENTER_SURNAME = State()
    ENTER_COURSE = State()
    ENTER_AGE = State()
    ENTER_PAYMENT = State()
    ENTER_CONTACT_NUMBER = State()
    #инициализация бота
    def __init__(self):
        self._TOKEN = '5689385764:AAFs8vZoZGrSYUN-kqkDifoj0I0lEZh1dnU'#токен
        self.bot = Bot(self._TOKEN)
        self.dp = Dispatcher(bot=self.bot, storage=MemoryStorage())
        self.memory = MemoryStorage()

    def start(self):
        #элементы клавиатуры (не к регистрации) не инлайн
        help_button = KeyboardButton('/help 🎫')
        price_button = KeyboardButton('/price 📠')
        info_button = KeyboardButton('/info 📊')
        pay_button = KeyboardButton('/reg 💵')
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(help_button, price_button, info_button, pay_button)
        #элементы клавиатуры (не к регистрации) инлайн
        inline_btn_intimeworkshop = InlineKeyboardButton('текущие мероприятия', callback_data='intime')
        inline_btn_lasttimeworkshop = InlineKeyboardButton('прошедшие мероприятия', callback_data='lastime')
        inline_keyboard_for_events = InlineKeyboardMarkup().add(inline_btn_intimeworkshop,inline_btn_lasttimeworkshop)
        #элементы клавиатуры (не к регистрации) инлайн
        inline_btn_infoevent1 = InlineKeyboardButton('мастер класс по росписи шоперов', callback_data='infoevent1')

        inline_keyboard_for_infoevents = InlineKeyboardMarkup().add(inline_btn_infoevent1)
        inline_keyboard_for_infoevents.add(InlineKeyboardButton('ссылка для оплаты мероприятия выше👆', url='https://www.tinkoff.ru/'))

        #команды
        @self.dp.message_handler(commands=['start'])
        async def hello(message: types.message):
            await message.answer('привет напиши /help что бы узнать список команд')

        @self.dp.message_handler(commands=['help'])
        async def hello(message: types.message):
            await message.answer('что умеет этот бот???\n/price - цены и информация о занятиях и группе\n/info - о нас \n если вы нашли ошибку просто очистие час с ботом и все!', reply_markup=keyboard)

        @self.dp.message_handler(commands=['price'])
        async def hello(message: types.message):
            await message.answer('Здравствуйте , выберите  какие конкретно мероприятия вас интересуют: ', reply_markup=inline_keyboard_for_events)

        @self.dp.callback_query_handler(lambda c: c.data == 'intime')
        async def process_callback_button1(callback_query: types.CallbackQuery):
            await callback_query.answer()
            await callback_query.message.answer('Вот текущие мероприятия:', reply_markup=inline_keyboard_for_infoevents)

        @self.dp.callback_query_handler(lambda c: c.data == 'infoevent1')
        async def process_button5_callback(callback_query: types.CallbackQuery):
            await callback_query.answer(text='это матстер класс по росписе шоперов хз что говорить еще)')

        @self.dp.callback_query_handler(lambda c: c.data == 'lastime')
        async def process_callback_button1(callback_query: types.CallbackQuery):
            await callback_query.answer()
            await callback_query.message.answer('Вот прошедшие мероприятия :\nмастер класс картина город')

        @self.dp.message_handler(commands=['info'])
        async def hello(message: types.message):
            await message.answer('', reply_markup=keyboard)

        #функция для регистрации
    def register(self):

        # Инициализируем клавиатуру
        keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button = KeyboardButton('нет ответа, перейти на следующий вопрос')
        menu_button = KeyboardButton('/menu')
        keyboard.add(button,menu_button)

        # Обработчик команды "/reg"
        @self.dp.message_handler(Command('reg'))
        async def start_reg(message: types.Message):
            await MyBot.ENTER_NAME.set()
            await message.answer('Введите имя ребенка:', reply_markup=keyboard)

        @self.dp.message_handler(state=MyBot.ENTER_NAME)
        async def process_name(message: types.Message, state: FSMContext):
            async with state.proxy() as data:
                data['name'] = message.text
            await MyBot.ENTER_SURNAME.set()
            await message.answer('Введите фамилию ребенка:', reply_markup=keyboard)

        @self.dp.message_handler(state=MyBot.ENTER_SURNAME)
        async def process_surname(message: Message,state: FSMContext):
            # Сохраняем фамилию ребенка и переходим на следующую стадию опроса
            async with state.proxy() as data:
                data['surname'] = message.text
            await MyBot.ENTER_COURSE.set()
            await message.answer('Введите курс или мероприятие на которое идет ребенок:', reply_markup=keyboard)

        @self.dp.message_handler(state=MyBot.ENTER_COURSE)
        async def process_course(message: Message, state: FSMContext):
            # Сохраняем курс/мероприятие и переходим на следующую стадию опроса
            async with state.proxy() as data:
                data['course'] = message.text
            await MyBot.ENTER_AGE.set()
            await message.answer('Введите возраст ребенка:', reply_markup=keyboard)

        @self.dp.message_handler(state=MyBot.ENTER_AGE)
        async def process_age(message: Message, state: FSMContext):
            # Сохраняем возраст ребенка и переходим на следующую стадию опроса
            async with state.proxy() as data:
                data['age'] = message.text
            await MyBot.ENTER_PAYMENT.set()
            await message.answer('Прошла ли у вас оплата ?', reply_markup=keyboard)

        @self.dp.message_handler(state=MyBot.ENTER_PAYMENT)
        async def process_payment(message: Message, state: FSMContext):
            # Сохраняем ответ пользователя на вопрос об оплате и переходим на следующую стадию опроса
            async with state.proxy() as data:
                data['payment'] = message.text
            await MyBot.ENTER_CONTACT_NUMBER.set()
            await message.answer('Напишите ваш контактный номер начиная с +7:', reply_markup=keyboard)

        @self.dp.message_handler(state=MyBot.ENTER_CONTACT_NUMBER)
        async def process_contact_number(message: Message, state: FSMContext):
            # Сохраняем контактный номер и выводим результат опроса
            async with state.proxy() as data:
                data['contact_number'] = message.text

                username = data['name']
                usersurname = data['surname']
                course = data['course']
                userage = data['age']
                pay = data['payment']
                contactnumber = data['contact_number']

                await message.answer(f"Ваша анкета успешно принята!\nВот ваши данные:\nИмя ребенка: {username}\nФамилия ребенка: {usersurname}\nКурс/мероприятие: {course}\nВозраст ребенка: {userage}\nОплата: {pay}\nКонтактный номер: {contactnumber} чтобы заполнить 2 анкету очистите чат с ботом \n чтобы выыйти из заполнения анкеты пропишите /menu " ,reply_markup=keyboard)
                conn.execute("INSERT INTO users (username, usersurname, course, userage, pay,contactnumber) VALUES (?, ?, ?, ?, ?, ?)",
                (username, usersurname, course, userage, pay, contactnumber))
                conn.commit()
                # Закрываем соединение с базой данных
                conn.close()                 
                print("человек завершил регистрацию!время :",time.ctime())
            await state.finish()
        @self.dp.message_handler(commands=['menu'])
        async def hello(message: types.message):
            await message.answer('/price\n/info\n/pay\n если вы нашли ошибку просто очистие час с ботом и все!', reply_markup=keyboard)
#запуск сервера
        executor.start_polling(self.dp, skip_updates=True)
#старт сервера
if __name__ == '__main__':
    bot = MyBot()
    bot.start()
    bot.register()

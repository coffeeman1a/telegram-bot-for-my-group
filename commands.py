
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from support import current_week
from lists import GROUPS, EMOJI
from random import randint

class Commands:
    def __init__(self, bot):
        self.bot = bot

        self.commands_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        self.commands_keyboard.add(
        KeyboardButton('помочь' + EMOJI['question_mark']),
        KeyboardButton('расписание' + EMOJI['calendar']),
        KeyboardButton('мой id' + EMOJI['eyes']),
        KeyboardButton('какая cейчас неделя' + EMOJI['thinking_face'],))
    
        self.weeks_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(text='Текущая неделя', callback_data='current week')],
            [InlineKeyboardButton(text='Следующая неделя', callback_data='next week')]])

        

    def start_message(self, message):
        if message.from_user.id not in self.bot.user_names or not self.bot.user_names[message.from_user.id]:
            if message.from_user.first_name:
                self.bot.user_names[message.from_user.id] = message.from_user.first_name
            else:
                self.bot.user_names[message.from_user.id] = message.from_user.username
            self.bot.save_config()
        self.bot.reply_to(message, 'Привет, ' + self.bot.user_names[message.from_user.id] + '! Я бот, впрочем как и мой разработчик.' + \
                          ' Снизу представлен список команд для вашего удобства.', reply_markup=self.commands_keyboard)
        self.bot.save_session(message)
    
    def help_message(self, message):
        self.bot.reply_to(message, 'Этот бот высылает расписание на неделю в формате iCalendar. Такой формат легко импортировать'+\
                          'в свой календарь. Чтобы получить список команд напишите /start')
        self.bot.save_session(message)
        
    def get_my_id(self, message):
        self.bot.reply_to(message, message.from_user.id)
        self.bot.save_session(message)
    
    def authorize_user(self, message=None, user_id=None):
        if message:
            if len(message.text.split()) < 2:
                self.bot.reply_to(message, 'Введите id пользователя.')
                return
            elif len(message.text.split()) > 2:
                self.bot.reply_to(message, 'Введите только id пользователя.')
                return
            elif not message.text.split()[1].isdigit():
                self.bot.reply_to(message, 'id пользователя должен быть числом.')
                return
            user_id = message.text.split()[1]
        if user_id:
            if user_id in self.bot.users:
                self.bot.config['users'][user_id] = 'authorized'
                self.bot.save_config()
                self.bot.reply_to(message, 'Пользователь с id ' + user_id + ' авторизован.')
                self.bot.send_message(user_id, 'Вы были успешно авторизованы!')
            else:
                self.bot.reply_to(message, 'Пользователь с таким id не найден.')
        
    
    def add_user(self, user_id):
        self.bot.users[user_id] = None
        self.bot.config['users'][str(user_id)] = self.bot.users[user_id]
        self.bot.save_config()
    
    def get_schedule_for_group(self, message):
        self.bot.send_message(message.chat.id, 'Напишите свою группу' + EMOJI['black_nib'] + '\nНапример: РИБО-03-20')
        self.bot.user_data[message.chat.id] = {}
        self.bot.save_session(message)
    
    def choose_week(self, message):
        self.bot.send_message(message.chat.id, 'Сейчас идёт ' + str(current_week()) + ' неделя. Выберете неделю.', reply_markup=self.weeks_keyboard)
        self.bot.user_data[message.chat.id]['group'] = message.text
        self.bot.save_session(message)
    
    def send_schedule(self, call):
        group = self.bot.user_data.get(call.message.chat.id, {}).get('group')
        week = call.data
        
        if call.data == 'current week':
            str_week = 'текущую'
        else:
            str_week = 'следующую'

        try:
            self.bot.send_document(call.message.chat.id, document=open(self.get_full_path(group, week), 'rb'), caption='Файл расписания на ' + str_week + ' неделю', reply_markup=None)
        except FileNotFoundError:
            self.bot.reply_to(call.message, 'Расписание не найдено. Возможно оно ещё не готово. Попробуйте позже.')

    def get_current_week(self, message):
        self.bot.reply_to(message, 'Сейчас идёт ' + str(current_week()) + ' неделя.')
        self.bot.save_session(message)

    def get_full_path(self, group, week):
        full_path = None
        p_week = None
        if week == 'current week':
            p_week = str(current_week())
        elif week == 'next week':
            p_week = str(current_week() + 1)

        full_path = 'timetables/' + group + '/timetable_' + GROUPS[group] + '_week_' + p_week + '.ics'
        if p_week:
            return full_path
    
    def coin_flip(self, message):
        self.bot.reply_to(message, ('Орёл.' if randint(0, 1) else 'Решка.'))
        self.bot.save_session(message)
    
    def show_info(self, message):
        self.bot.reply_to(message, 'Это любительский проект, который был создан для удобства студентов РИБО. Разработчик: а где')
        self.bot.save_session(message)
    
    def uknown_message(self, message):
        self.bot.reply_to(message, EMOJI['face with open mouth vomiting'])

    def unauthorized_users(self, message):
        unauthorized_users = []
        for user_id, status in self.bot.users.items():
            if status != 'authorized':
                unauthorized_users.append(user_id + '\n')
        if unauthorized_users:
            self.bot.send_message(message.chat.id, 'Список неавторизованных пользователей:\n' + ''.join(unauthorized_users))
        else:
            self.bot.send_message(message.chat.id, 'Неавторизованных пользователей не найдено.')
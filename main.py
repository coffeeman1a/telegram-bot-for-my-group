import os
from commands import Commands
from bot import TelegramBot
from lists import GROUPS

if __name__ == '__main__':

    bot = TelegramBot(os.environ["TELEGRAM_API_KEY"],
                        config_file='config.json',
                        session_file='session.json')
    

    command = Commands(bot)

    def restricted(func):
        def wrapped(message):
            user_id = str(message.from_user.id)
            if user_id not in bot.users or not bot.users[user_id]:
                    command.add_user(user_id)
            if bot.users[user_id] != 'authorized':
                bot.reply_to(message, "Вы не авторизованы для использования этой команды." + \
                            'Это небольшой проект, поэтому авторизация происходит вручную.' + \
                            'Напишите комманду /info, чтобы получить контакты разработчика')
                return
            return func(message)      
        return wrapped

    def admin(func):
        def wrapped(message):
            user_id = str(message.from_user.id)
            if user_id not in bot.admins or not bot.admins[user_id]:
                bot.reply_to(message, "Вы не администратор.")
                return
            return func(message)      
        return wrapped
    

    @bot.message_handler(commands=['start'])
    @restricted
    def start_message(message):
        command.start_message(message)

    @bot.message_handler(regexp='помочь')
    @restricted
    def help_message(message):
        command.help_message(message)

    @bot.message_handler(regexp='мой id')
    def get_my_id(message):
        command.get_my_id(message)
    
    @bot.message_handler(commands=['authorize_user'])
    @admin
    def authorize_user(message):
        command.authorize_user(message)
    
    @bot.message_handler(commands=['unauthorized_users'])
    @admin
    def unauthorized_users(message):
        command.unauthorized_users(message)
    
    @bot.message_handler(regexp='расписание')
    @restricted
    def handle_group_schedule(message):
        command.get_schedule_for_group(message)

    @bot.message_handler(func=lambda message: message.text in GROUPS)
    @restricted
    def handle_week_schedule(message):
        command.choose_week(message)
    
    @bot.callback_query_handler(func=lambda call: True)
    @restricted
    def callback_handler(call):
        command.send_schedule(call)

    @bot.message_handler(regexp='какая cейчас неделя?')
    @restricted
    def get_current_week(message):
        command.get_current_week(message)
    
    @bot.message_handler(commands=['coin'])
    @restricted
    def coin_flip(message):
        command.coin_flip(message)
    
    @bot.message_handler(commands=['info'])
    def show_info(message):
        command.show_info(message)

    @bot.message_handler()
    def unknown_message(message):
       command.uknown_message(message)

    bot.polling()
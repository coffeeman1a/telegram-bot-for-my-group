import telebot
from support import load_session, save_session, load_config, save_config

class TelegramBot(telebot.TeleBot):
    def __init__(self, token, config_file=None, session_file=None):
        super().__init__(token)
        self.session_file = session_file
        self.config_file = config_file
        self.session = load_session(session_file)
        self.config = load_config(config_file)
        self.user_data = {}
        self.users = []
        self.admins = []
        self.user_names = []
        self.update_users()
        print(self.config)
        

    def update_users(self):
        self.config.setdefault('admins', [])
        self.config.setdefault('users', [])
        self.config.setdefault('user_names', [])

        self.users = self.config.get('users', [])
        self.admins = self.config.get('admins', [])
        self.user_names = self.config.get('user_names', [])
        
    def save_session(self, message):
        print(save_session(message, self.session, self.session_file))
    
    def save_config(self):
        save_config(self.config, self.config_file)
        self.update_users()
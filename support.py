import json, datetime
import os

#загрузка сессии
def load_session(session_file='session.json'):
    session = {}
    if session_file and os.path.exists(session_file) and not os.stat(session_file).st_size == 0:
            with open(session_file, 'r') as f:
                session = json.load(f)
    else:
        with open(session_file, 'x') as f:
            json.dump(session, f)
    return session   

#запись сессии
def save_session(message, session, session_file='session.json'):
    if all((session_file, session)) != None:
            if message.chat.id not in session:
                session[message.chat.id] = {'history': []}
            session[message.chat.id]['history'].append({
                 'text': message.text,
                 'date': time(message)})

            with open(session_file, 'w') as f:
                json.dump(session, f)
            return True

#загрузка конфига
def load_config(config_file='config.json'):
    config = {}
    if config_file and os.path.exists(config_file) and not os.stat(config_file).st_size == 0:
        with open(config_file, 'r') as f:
            config = json.load(f)
    else:
        with open(config_file, 'x') as f:
            json.dump(config, f)
    return config

#запись конфига
def save_config(config, config_file='config.json'):
    if config:
        with open(config_file, 'w') as f:
            json.dump(config, f)
        return True

#конвертация времени
def time(message):
    timestamp = message.date
    datetime_str = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    return datetime_str

def current_week():
    
    start_date = datetime.date(2023, 2, 6)
    current_date = datetime.date.today()
    days_since_start = (current_date - start_date).days
    current_week = days_since_start // 7 + 1

    return current_week
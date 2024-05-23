import os
from dotenv import load_dotenv

# Завантажимо дані середовища з файлу .env(За замовчуванням)
load_dotenv()


# Дістанемо токен бота з середовища
bot_token = os.getenv('BOT_TOKEN')


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE_DIR, 'app', 'data', 'data_films.json')

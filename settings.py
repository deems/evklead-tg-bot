from environs import Env

env = Env()
env.read_env()  # read .env file, if it exists

BOT_TOKEN = env("BOT_TOKEN")
# required variables
REDIS_URL = env("REDIS_URL")

LANG = env('LANG', 'ru')

IS_LOCAL = env('IS_LOCAL', False)

CHAT_FOR_NEWS = env('CHAT_FOR_NEWS')

RSS_URL = 'https://www.google.ru/alerts/feeds/12027305867459824764/2965769019592255919'

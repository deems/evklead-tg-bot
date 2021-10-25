import logging

from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import settings
from services.bot_service import bot_service
from services.news_service.news_service import news_service
from services.score_service.score_service import score_service

bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)


def register_handlers():
    dp.register_message_handler(bot_service.on_new_user, content_types=['new_chat_members'])
    dp.register_message_handler(bot_service.welcome, commands=['start', 'help'])
    dp.register_message_handler(news_service.top_news, commands=['news'])
    dp.register_message_handler(score_service.get_top, commands=['cats_top'])
    dp.register_message_handler(score_service.update_score, regexp='спасибо|\+')
    # dp.register_message_handler(bot_service.echo)


if __name__ == '__main__':
    register_handlers()

    executor.start_polling(dp, skip_updates=True)

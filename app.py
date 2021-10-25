import logging
import os

from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.utils.executor import start_webhook

import settings
from services.bot_service import bot_service
from services.news_service.news_service import news_service
from services.score_service.score_service import score_service

bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)

WEBHOOK_HOST = 'https://evklead-tg-bot.herokuapp.com/'
WEBHOOK_PATH = '/webhook/' + settings.BOT_TOKEN
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"


def register_handlers():
    dp.register_message_handler(bot_service.on_new_user, content_types=['new_chat_members'])
    dp.register_message_handler(bot_service.welcome, commands=['start', 'help'])
    dp.register_message_handler(news_service.top_news, commands=['news'])
    dp.register_message_handler(score_service.get_top, commands=['cats_top'])
    dp.register_message_handler(score_service.update_score, regexp='спасибо|\+')
    # dp.register_message_handler(bot_service.echo)


async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)


async def on_shutdown(dp):
    logging.warning('Shutting down..')

    # insert code here to run it before shutdown

    # Remove webhook (not acceptable in some cases)
    await bot.delete_webhook()

    logging.warning('Bye!')


if __name__ == '__main__':
    register_handlers()

    if settings.IS_LOCAL:
        executor.start_polling(dp, skip_updates=True)
    else:
        start_webhook(
            dispatcher=dp,
            webhook_path=WEBHOOK_PATH,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            skip_updates=True,
            host='0.0.0.0',
            port=os.getenv('PORT'),
        )

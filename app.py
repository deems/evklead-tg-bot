import asyncio
import logging

import aioschedule
from aiogram.utils import executor

from bot import dp
from services.bot_service import bot_service
from services.news_service.news_service import news_service
from services.score_service.score_service import score_service

logging.basicConfig(level=logging.INFO)


def register_handlers():
    dp.register_message_handler(bot_service.on_new_user, content_types=['new_chat_members'])
    dp.register_message_handler(bot_service.welcome, commands=['start', 'help'])
    #dp.register_message_handler(news_service.top_news, commands=['news'])
    dp.register_message_handler(score_service.get_top, commands=['cats_top'])
    dp.register_message_handler(score_service.update_score, regexp='спасибо|\+')
    # dp.register_message_handler(bot_service.echo)


async def scheduler():
    aioschedule.every().hour.at(":00").do(news_service.send_top_news)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(_):
    asyncio.create_task(scheduler())


if __name__ == '__main__':
    register_handlers()

    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

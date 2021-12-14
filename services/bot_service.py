from aiogram import types

from services.likes_service.like_service import like_service
from services.locales_service.locales_service import locales_service


class BotService:
    async def on_new_user(self, message: types.Message):
        user_name = '@' + message.new_chat_members[0].username \
            if message.new_chat_members[0].username \
            else message.new_chat_members[0].full_name
        new_user_message = locales_service.get_key('hello_message', userName=user_name)
        await message.reply(new_user_message, disable_web_page_preview=True)

    async def echo(self, message: types.Message):
        buttons = await like_service.get_likes_buttons()
        await message.reply(message.text, reply_markup=buttons)

    async def welcome(self, message: types.Message):
        help_message = locales_service.get_key('help')
        await message.reply(help_message)


bot_service = BotService()

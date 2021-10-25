from aiogram import types

from services.locales_service.locales_service import locales_service


class BotService:
    async def on_new_user(self, message: types.Message):
        new_user_message = locales_service.get_key('hello_message', userName=message.new_chat_members[0].username)
        await message.reply(new_user_message)

    async def echo(self, message: types.Message):
        if 'привет' in message.text:
            response = 'хуивет'
        else:
            response = message.text
        await message.reply(f'{response}')

    async def welcome(self, message: types.Message):
        pass


bot_service = BotService()

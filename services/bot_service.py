from aiogram import types

from services.locales_service.locales_service import locales_service


class BotService:
    async def on_new_user(self, message: types.Message):
        user_name = '@'+message.new_chat_members[0].username \
            if message.new_chat_members[0].username \
            else message.new_chat_members[0].full_name
        new_user_message = locales_service.get_key('hello_message', userName=user_name)
        await message.reply(new_user_message)

    async def echo(self, message: types.Message):
        if 'привет' in message.text:
            response = 'хуивет'
        else:
            response = message.text
        await message.reply(f'{response}')

    async def welcome(self, message: types.Message):
        help_message = locales_service.get_key('help')
        await message.reply(help_message)


bot_service = BotService()

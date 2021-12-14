from typing import Optional

from aiogram import types
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from bot import bot
from redis_pool import redis
from services.likes_service.data.like_type import ActionType


class LikeService:
    def __init__(self):
        self.callback_likes = CallbackData("likes", "action")
        self._likes_prefix = 'likes_count_'
        self._already_like_prefix = 'already_like_'

    async def _incr_count(self, action_type: ActionType, chat_id: int, message_id: int, user_id: int) -> Optional[int]:
        already_like_key = f'{self._already_like_prefix}-{chat_id}-{message_id}-{action_type.value}{user_id}'
        already_like = await redis.get(already_like_key)
        if already_like:
            return None

        count = await redis.incr(f'{self._likes_prefix}-{chat_id}-{message_id}-{action_type.value}')
        await redis.set(already_like_key, 1, 3600 * 24 * 15)
        return count

    async def _get_likes(self, action_type: ActionType, chat_id: int, message_id: int) -> int:
        count = await redis.get(f'{self._likes_prefix}-{chat_id}-{message_id}-{action_type.value}')
        if not count:
            return 0
        return count

    async def get_likes_buttons(self, chat_id: int = None, message_id: int = None) -> InlineKeyboardMarkup:
        keyboard = types.InlineKeyboardMarkup(row_width=2)

        likes_count = dislikes_count = None
        if chat_id and message_id:
            likes_count = await self._get_likes(ActionType.LIKE, chat_id, message_id)
            dislikes_count = await self._get_likes(ActionType.DISLIKE, chat_id, message_id)

        buttons = [types.InlineKeyboardButton(text=f"🔥 {likes_count if likes_count else ''}",
                                              callback_data=self.callback_likes.new(action=ActionType.LIKE.value)),
                   types.InlineKeyboardButton(text=f"💩 {dislikes_count if dislikes_count else ''}",
                                              callback_data=self.callback_likes.new(action=ActionType.DISLIKE.value))]
        keyboard.row(*buttons)

        return keyboard

    async def like_query_handler(self, call: types.CallbackQuery, callback_data: dict):
        action = ActionType(callback_data['action'])

        res = await self._incr_count(action, call.message.chat.id, call.message.message_id, call.from_user.id)

        if not res:
            # уже голосовал
            await call.answer()
            return
        buttons = await self.get_likes_buttons(call.message.chat.id, call.message.message_id)

        await bot.edit_message_text(text=call.message.text, message_id=call.message.message_id,
                                    chat_id=call.message.chat.id, reply_markup=buttons)


like_service = LikeService()

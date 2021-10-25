import re
from typing import List, Tuple

import pymorphy2
from aiogram import types

from redis_pool import redis
from services.locales_service.locales_service import locales_service

morph = pymorphy2.MorphAnalyzer()


class ScoreService:
    def __init__(self):
        self.username_regex = re.compile(r'@([A-Za-z0-9_]+)')
        self.top_name = 'cats_top'
        self.cats_morph = morph.parse(locales_service.get_key('score_top_noun'))[0]

    async def update_score(self, message: types.Message):
        all_users_names = self.username_regex.findall(message.text)
        if all_users_names:
            username = all_users_names[0]
            antispam_key = f'score_spam_ttl_{message.from_user.id}{username}'
            spam = await redis.get(antispam_key)
            if spam:
                await message.reply(locales_service.get_key('antispam_message'))
                return

            await redis.zincrby(f'{self.top_name}_{message.chat.id}', 1, username)

            answer = locales_service.get_key('update_score_response', userName=username)
            await message.answer(answer)
            await redis.set(antispam_key, 1, 60)

    async def get_top(self, message: types.Message):
        scores: List[Tuple[bytes, float]] = await redis.zrevrangebyscore(f'{self.top_name}_{message.chat.id}',
                                                                         '+inf',
                                                                         0,
                                                                         withscores=True)
        if scores:
            scores_list: List[str] = []
            for user_score in scores:
                score = round(user_score[1])
                scores_list.append(locales_service.
                                   get_key('score_top_item',
                                           userName=user_score[0].decode(),
                                           catsCount=score,
                                           catsMorph=self.cats_morph.make_agree_with_number(score).word))
            reply = '\n'.join(scores_list)
        else:
            reply = locales_service.get_key('score_top_empty')

        await message.reply(reply)


score_service = ScoreService()

import re
from typing import List

import aiohttp
import feedparser
from aiogram import types

import settings
from bot import bot
from redis_pool import redis
from services.locales_service.locales_service import locales_service
from services.news_service.data.news_item import NewsItem


class NewsService:
    def __init__(self):
        self.rss_url = settings.RSS_URL
        self.news_max_count = 3

    async def _get_rss(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.rss_url, ssl=False) as resp:
                return await resp.text()

    async def _process_news(self) -> List[NewsItem]:
        xml = await self._get_rss()
        feed = feedparser.parse(xml)

        result: List[NewsItem] = []
        last_news_id = await redis.get('last_news_id')

        for item in feed['items']:
            if last_news_id and last_news_id == item['id']:
                break
            news_item = NewsItem(
                text=locales_service.get_key("news_item",
                                             title=item["title"],
                                             content=re.sub('<[^<]+?>', '', item["content"][0]['value']),
                                             link=item["link"])
            )
            result.append(news_item)
            if len(result) >= self.news_max_count:
                break
        if result:
            # сохраним id самой свежей новости
            await redis.set('last_news_id', feed['items'][0]['id'])
        return result

    async def top_news(self, message: types.Message):
        news = await self._process_news()
        if news:
            #buttons = await like_service.get_likes_buttons()
            for item in news:
                await bot.send_message(message.chat.id, item.text,
                                       parse_mode=types.ParseMode.HTML)

    async def send_top_news(self):
        news = await self._process_news()
        if news:
            #buttons = await like_service.get_likes_buttons()
            for item in news:
                await bot.send_message(settings.CHAT_FOR_NEWS, item.text,
                                       parse_mode=types.ParseMode.HTML)


news_service = NewsService()

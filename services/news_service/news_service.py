import hashlib
import re
from typing import List

import aiohttp
import feedparser
from aiogram import types

import settings
from bot import bot
from redis_pool import redis
from services.likes_service.like_service import like_service
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
            if last_news_id and last_news_id == hashlib.md5(item['link'].encode('utf-8')).hexdigest():
                break
            news_item = NewsItem(
                text=locales_service.get_key("news_item",
                                             title=item["title"],
                                             content=re.sub('<[^<]+?>', '', item["description"]),
                                             link=item["link"]),
                img_url=item['media_content'][0]['url']
            )
            result.append(news_item)
            if len(result) >= self.news_max_count:
                break
        if result:
            # сохраним id самой свежей новости
            await redis.set('last_news_id', hashlib.md5(feed['items'][0]['link'].encode('utf-8')).hexdigest())
        return result

    async def top_news(self, message: types.Message):
        news = await self._process_news()
        if news:
            buttons = await like_service.get_likes_buttons()
            for item in news:
                await bot.send_photo(message.chat.id, item.img_url,
                                     caption=item.text,
                                     parse_mode=types.ParseMode.HTML,
                                     reply_markup=buttons)

    async def send_top_news(self):
        news = await self._process_news()
        if news:
            buttons = await like_service.get_likes_buttons()
            for item in news:
                await bot.send_photo(settings.CHAT_FOR_NEWS, item.img_url,
                                     caption=item.text,
                                     parse_mode=types.ParseMode.HTML,
                                     reply_markup=buttons)


news_service = NewsService()

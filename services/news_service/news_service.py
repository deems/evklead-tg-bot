import logging
from typing import List

import aiohttp
import feedparser
from aiogram import types

from services.locales_service.locales_service import locales_service


class NewsService:
    def __init__(self):
        self.rss_url = 'https://www.google.ru/alerts/feeds/12027305867459824764/2965769019592255919'

    async def _get_rss(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.rss_url, ssl=False) as resp:
                return await resp.text()

    async def _process_news(self) -> List[str]:
        xml = await self._get_rss()
        feed = feedparser.parse(xml)

        result: List[str] = []
        for item in feed['items']:
            logging.info(item["content"][0]["value"])
            result.append(locales_service.get_key("news_item",
                                                  title=item["title"],
                                                  content=item["content"][0]["value"],
                                                  link=item["link"]))
            if len(result) > 3:
                break

        return result

    async def top_news(self, message: types.Message):
        news = await self._process_news()
        await message.reply(''.join(news), parse_mode=types.ParseMode.HTML)


news_service = NewsService()

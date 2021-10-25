import json
from pathlib import Path
from typing import Optional

import settings
from services.locales_service.exceptions.locales_exception import LocalesException


class LocalesService:
    def __init__(self):
        self.default_lang = 'ru'
        self.lang = settings.LANG
        self.locales = {}
        for path in Path('locales').iterdir():
            locale_name = path.stem
            with path.open() as f:
                c = f.read()
                self.locales[locale_name] = json.loads(c)
        if not self.locales.get(self.default_lang):
            raise LocalesException(f'not found default lang {self.default_lang}')

    def get_key(self, key: str, **kwargs) -> Optional[str]:
        if self.lang in self.locales:
            result = self.locales[self.lang].get(key)
        else:
            result = self.locales[self.default_lang].get(key)
        if result:
            for key, val in kwargs.items():
                result = result.replace(f'%{key}%', str(val))

        return result


locales_service = LocalesService()

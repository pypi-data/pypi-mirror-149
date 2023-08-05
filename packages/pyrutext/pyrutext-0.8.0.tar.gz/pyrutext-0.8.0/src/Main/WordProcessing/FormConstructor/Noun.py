from typing import Awaitable, Callable
from .. import Defines


class Noun():

    def __init__(self, ask_method: Callable[[str, tuple[str, ...]], Awaitable[str]]):
        self.__ask_method = ask_method

    async def declined(self, word: str, *args, path=()):
        return {
            Defines.default: await self.case(word, *args, 'и.п.', path=path + ('Именительный падеж', )),
            'р.п.': await self.case(word, *args, 'р.п.', path=path + ('Родительный падеж', )),
            'д.п.': await self.case(word, *args, 'д.п.', path=path + ('Дательный падеж', )),
            'в.п.': await self.case(word, *args, 'в.п.', path=path + ('Винительный падеж', )),
            'т.п.': await self.case(word, *args, 'т.п.', path=path + ('Творительный падеж', )),
            'п.п.': await self.case(word, *args, 'п.п.', path=path + ('Предложный падеж', ))
        }

    async def case(self, word: str, *args, path=()):
        if 'ед.ч.' in args or 'мн.ч.' in args:
            return '+' if 'и.п.' in args else await self.__ask_method(word, path)

        return {
            Defines.default: '+' if 'и.п.' in args else await self.__ask_method(word, path + ('единственное число', )),
            'мн.ч.': await self.__ask_method(word, path + ('множественное число', ))
        }

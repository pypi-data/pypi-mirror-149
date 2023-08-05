from typing import Awaitable, Callable
from .. import Defines


class Adj():

    def __init__(self, ask_method: Callable[[str, tuple[str, ...]], Awaitable[str]]):
        self.__ask_method = ask_method

    async def singular(self, word: str, *, path=()):
        mascul_neu_preset = {
            'р.п.': await self.__ask_method(word, path=path + ('мужской/средний род', 'родительный падеж')),
            'д.п.': await self.__ask_method(word, path=path + ('мужской/средний род', 'дательный падеж')),
            'т.п.': await self.__ask_method(word, path=path + ('мужской/средний род', 'творительный падеж')),
            'п.п.': await self.__ask_method(word, path=path + ('мужской/средний род', 'предложный падеж'))
        }

        mascul_preset = mascul_neu_preset.copy()
        mascul_preset[Defines.default] = '+'
        mascul_preset['в.п.'] = {
            Defines.default: mascul_preset[Defines.default],
            'одуш.': mascul_preset['р.п.']
        }

        neu_preset = mascul_neu_preset.copy()
        neu_preset[Defines.default] = await self.__ask_method(word, path=path + ('средний род', 'именительный падеж'))
        neu_preset['в.п.'] = {
            Defines.default: neu_preset[Defines.default],
            'одуш.': neu_preset['р.п.']
        }

        fem_case = await self.__ask_method(word, path=path + ('женский род', 'родительный/дательный/творительный/предложный падеж'))

        return {
            Defines.default: mascul_preset,
            'с.р.': neu_preset,
            'ж.р.': {
                Defines.default: await self.__ask_method(word, path=path + ('женский род', 'именительный падеж')),
                'р.п.': fem_case,
                'д.п.': fem_case,
                'в.п.': await self.__ask_method(word, path=path + ('женский род', 'винительный падеж')),
                'т.п.': fem_case,
                'п.п.': fem_case
            }
        }

    async def plural(self, word: str, *, path=()):
        nominative = await self.__ask_method(word, path=path + ('именительный падеж', ))
        genitive = await self.__ask_method(word, path=path + ('родительный падеж', ))
        return {
            Defines.default: nominative,
            'р.п.': genitive,
            'д.п.': await self.__ask_method(word, path=path + ('дательный падеж', )),
            'в.п.': {
                Defines.default: nominative,
                'одуш.': genitive
            },
            'т.п.': await self.__ask_method(word, path=path + ('творительный падеж', )),
            'п.п.': await self.__ask_method(word, path=path + ('предложный падеж', )),
        }

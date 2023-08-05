from typing import Awaitable, Callable
from .. import Defines


class Verb():

    def __init__(self, ask_method: Callable[[str, tuple[str, ...]], Awaitable[str]]):
        self.__ask_method = ask_method

    async def imperative(self, word: str, *, path=()):
        imperative_form = await self.__ask_method(word, path)
        return {
            Defines.default: imperative_form,
            'мн.ч.': imperative_form + 'те'
        }

    async def conjugable(self, word: str, *args, path=()):
        forms = {}

        forms[Defines.default] = '+'
        forms['п.в.'] = await self.time_past(word, path=path + ('Прошедшее время', ))
        forms['б.в.'] = await self.time(word, *args, 'б.в.', path=path + ('Будущее время', ))
        if 'несов.' in args:
            forms['н.в.'] = await self.time(word, *args, 'н.в.', path=path + ('Настоящее время', ))

        return forms

    async def time_past(self, word: str, *, path=()):
        forms = {}

        standard_form = await self.__ask_method(word, path)

        forms[Defines.default] = standard_form  # мужской род
        if standard_form[-1] != 'л':
            standard_form = standard_form + 'л'
        forms['ж.р.'] = standard_form + 'а'
        forms['с.р.'] = standard_form + 'о'
        forms['мн.ч.'] = standard_form + 'и'

        return forms

    async def time(self, word: str, *args, path=()):
        return {
            Defines.default: '+',
            '1л': await self.person(word, *args, '1л', path=path + ('первое лицо', )),
            '2л': await self.person(word, *args, '2л', path=path + ('второе лицо', )),
            '3л': await self.person(word, *args, '3л', path=path + ('третье лицо', ))
        }

    async def person(self, word: str, *args, path=()):
        if 'б.в.' in args and 'несов.' in args:
            return {
                Defines.default: 'буду +',
                'мн.ч.': 'будем +'
            } if '1л' in args else {
                Defines.default: 'будешь +',
                'мн.ч.': 'будете +'
            } if '2л' in args else {
                Defines.default: 'будет +',
                'мн.ч.': 'будут +'
            }

        return {
            Defines.default: await self.__ask_method(word, path=path + ('единственное число', )),
            'мн.ч.': await self.__ask_method(word, path=path + ('множественное число', ))
        }

from .. import Defines
from typing import Awaitable, Callable
from .Adj import Adj
from .Noun import Noun
from .Verb import Verb


def lookup(self, *args):
    if type(self) is not dict:
        return self

    default_key = Defines.default if Defines.default_key not in self else self[Defines.default_key]

    for arg in args:
        if arg in self:
            return lookup(self[arg], *args)

    value = self[default_key]
    return lookup(value, *args)


def tags(self: dict, word: str):
    if Defines.tags_key in self[word]:
        return self[word][Defines.tags_key]
    return []


async def construct(word: str, *args, path=(), ask_method: Callable[[str, tuple[str, ...]], Awaitable[str]]):
    if len(args) == 0:
        return '+'

    origin = {
        Defines.tags_key: list(args)
    }

    if 'гл.' in args:
        return {
            **origin,
            Defines.default: await Verb(ask_method).conjugable(word, *args, path=path),
            'пов.': await Verb(ask_method).imperative(word, path=path + ('Повелительное наклонение', )),
            'инф.': '+'
        }
    elif 'сущ.' in args:
        return {
            **origin,
            Defines.default: '+' if 'нескл.' in args else await Noun(ask_method).declined(word, *args, path=path)
        }
    elif 'пр.' in args:
        return {
            **origin,
            Defines.default: await Adj(ask_method).singular(word, path=path + ('Единственное число', )),
            'мн.ч.': await Adj(ask_method).plural(word, path=path + ('Множественное число', ))
        }
    else:
        return {
            **origin,
            Defines.default: '+'
        }

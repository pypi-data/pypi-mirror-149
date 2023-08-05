from .Util.Util import extract_all, rel_format
from . import Defines
from .FormConstructor import FormConstructor
from typing import Awaitable, Callable
import random
from dataclasses import dataclass, field
import enum


class ErrorGrade(enum.Enum):
    OK = enum.auto()
    WARNING = enum.auto()
    ERROR = enum.auto()


class WordDictStatus(enum.Enum):
    OK = enum.auto()
    INVALID_REFERENCE = enum.auto()
    REFERENCE_ALREADY_SET = enum.auto()
    WORD_ALREADY_EXISTS = enum.auto()
    NO_TAGS = enum.auto()
    GOT_PHRASE = enum.auto()
    NOUN_NO_GENDER = enum.auto()
    VERB_NO_PERFECTNESS = enum.auto()
    NO_WORD_FOUND = enum.auto()
    FORM_EXCEPTION = enum.auto()


@dataclass
class WordDictResponse:
    word: str
    tags: list[str] = field(default_factory=list)
    grade: ErrorGrade = ErrorGrade.OK
    status: WordDictStatus = WordDictStatus.OK
    supplement: str = ''


@dataclass
class WordDictFormRequest:
    word: str
    forms: list[str] = field(default_factory=list)


class WordDict:

    __word_types = ('безл.', )
    __word_traits = ('абр', 'пинг', 'перс')

    def __init__(self, storage):
        self.__words = storage('words')

    def delete(self, *args):
        for name in args:
            del self.__words[name]

    def get(self, *args, to_format=True):
        tags = list(args)

        forms = extract_all(tags, 'ед.ч.', 'мн.ч.', 'и.п.', 'р.п.', 'д.п.', 'в.п.', 'т.п.', 'п.п.', 'п.в.', 'н.в.', 'б.в.', '1л', '2л', '3л', to_pop=True)

        if 'гл.' in args:
            forms.extend(extract_all(tags, 'инф.', 'пов.', 'м.р.', 'с.р.', 'ж.р.', to_pop=True))
        elif 'пр.' in args:
            forms.extend(extract_all(tags, 'одуш.', 'неодуш.', 'м.р.', 'с.р.', 'ж.р.', to_pop=True))

        tag_correlations = tuple(filter(
            lambda word: all(tag in FormConstructor.tags(self.__words, word) for tag in tags), self.__words.keys()
            )) if len(tags) > 0 else tuple(self.__words.keys())

        if len(tag_correlations) == 0:
            return None

        word = random.choice(tag_correlations)

        return rel_format(word, FormConstructor.lookup(self.__words[word], *forms)) if to_format else word

    def get_form(self, word: str, *args):
        return rel_format(word, FormConstructor.lookup(self.__words[word], *args))

    async def flush(self):
        await self.__words.flush()

    async def save(self):
        await self.__words.save()

    def check(self, word: str, tags: list[str]) -> WordDictResponse:
        types = extract_all(tags, *self.__word_types, to_pop=True)
        for word_type in types:
            if word_type == 'безл.':
                tags.extend(('м.р.', 'ж.р.'))

        traits = extract_all(tags, *self.__word_traits, to_pop=False)
        for word_trait in traits:
            if word_trait in ('абр', 'пинг'):
                tags.append('нескл.')
            elif word_trait == 'перс':
                tags.append('ед.ч.')

        tags = list(set(tags))

        response = WordDictResponse(word, tags)
        reference = None
        for tag in tags:
            if tag[0] == '&':
                reference_to = tag[1:]
                if reference_to not in self.__words:
                    return WordDictResponse(word, tags, ErrorGrade.ERROR, WordDictStatus.INVALID_REFERENCE, reference_to)
                else:
                    if reference is not None:
                        response.grade = ErrorGrade.WARNING
                        response.status = WordDictStatus.REFERENCE_ALREADY_SET
                        response.supplement = str((reference, reference_to))
                    reference = reference_to

        if word in self.__words:
            response.grade = ErrorGrade.WARNING
            response.status = WordDictStatus.WORD_ALREADY_EXISTS
            response.supplement = str(FormConstructor.tags(self.__words, word))
        elif 'сущ.' in tags:
            if 'м.р.' not in tags and 'с.р.' not in tags and 'ж.р.' not in tags:
                response.grade = ErrorGrade.WARNING
                response.status = WordDictStatus.NOUN_NO_GENDER
        elif len(word.split()) > 1:
            response.grade = ErrorGrade.WARNING
            response.status = WordDictStatus.GOT_PHRASE

        if 'гл.' in tags:
            if 'сов.' not in tags and 'несов.' not in tags:
                response.grade = ErrorGrade.ERROR
                response.status = WordDictStatus.VERB_NO_PERFECTNESS
        elif len(tags) == 0:
            response.grade = ErrorGrade.ERROR
            response.status = WordDictStatus.NO_TAGS

        return response

    async def insert(self, word: str, tags: list[str], /, ask_method: Callable[[str, tuple[str, ...]], Awaitable[str]]):
        response = self.check(word, tags)
        if response.grade != ErrorGrade.ERROR:
            reference = list(filter(lambda s: (s[0] == '&'), tags))
            if reference == []:
                self.__words[word] = await FormConstructor.construct(word, *tags, ask_method=ask_method)
            else:
                reference = reference[-1]
                if len(tags) == 1:
                    self.__words[word] = self.__words[reference]
                else:
                    tags.remove('&' + reference)
                    self.__words[word] = dict(self.__words[reference])
                    self.__words[word][Defines.tags_key] = tags

        return response

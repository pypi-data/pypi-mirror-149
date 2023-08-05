import re
from typing import Any, Awaitable, Callable, List, Tuple
import aioconsole
import asyncio

from Main.WordProcessing.WordDict import *
from Main.TextProcessing.TextDict import *
from Main.TextProcessing.Render import *


class Session():
    def __init__(self, id: str):
        self.input_trigger = asyncio.Event()
        self.__buf: str = str()
        self.id = id

    def output(self, cmd: str):
        self.__buf = cmd.strip()
        self.input_trigger.set()
        self.input_trigger.clear()

    async def input(self) -> str:
        await self.input_trigger.wait()
        return self.__buf

    def print(self, text: Any = '', *, end: str = '\n'):
        text = str(text)
        if self.id != '':
            indent = ' ' * len('[' + self.id + '] ')
            print('[' + self.id + ']', end=' ')
            text = text.replace('\n', '\n' + indent)
        print(text, end=end)

    def debug(self, text: Any = '', *, end: str = '\n'):
        text = str(text)
        if self.id != '':
            indent = '-' * len('{' + self.id + '}') + ' '
            print('{' + self.id + '}', end=' ')
            text = text.replace('\n', '\n' + indent)
        print(text, end=end)


class SessionCtl():
    sessions = dict()
    __cmd: dict[str, Callable[..., Awaitable[Any]]] = dict()
    details: dict[str, str] = dict()
    __last_prefix: str = ''

    @classmethod
    def halt(cls, ssn: Session, *args):
        if len(args) != 0:
            ssn.debug(f'Halted.\nReturned: {args}')
        del cls.sessions[ssn.id]

    @classmethod
    def new(cls, id: str, start: list = []):
        cls.sessions[id] = Session(id)
        cmd = '' if len(start) < 1 else start[0]
        args = [] if len(start) < 2 else start[1:]
        try:
            asyncio.create_task(cls.__cmd[cmd](cls.sessions[id], *args))
        except KeyError:
            asyncio.create_task(cls.__cmd[''](cls.sessions[id]))
        except TypeError:
            asyncio.create_task(cls.__cmd[''](cls.sessions[id], cmd))

    @classmethod
    def input(cls, cmd: str):
        if cmd == '':
            id = cls.__last_prefix
            text = []
        else:
            tokens = cmd.split()
            if tokens[0].startswith(':'):
                id = '' if len(tokens[0]) == 1 else tokens[0][1:]
                text = tokens[1:]
                cls.__last_prefix = id
            else:
                id = cls.__last_prefix
                text = tokens

        if id not in cls.sessions:
            cls.new(id, text)
        else:
            cls.sessions[id].output(' '.join(text))

    @classmethod
    def define_cmd(cls, methodlist: List[Tuple[str, Callable[..., Awaitable[Any]], str]]):
        for record in methodlist:
            cls.__cmd[record[0]] = record[1]
            cls.details[record[0]] = record[2]


class AShell():

    __wordctl: WordDict
    __textctl: TextDict
    __renderer: Renderer

    @classmethod
    async def get_text(cls, ssn: Session):
        template = cls.__textctl.get('')
        text, render_result = cls.__renderer.render(template)

        for exception in render_result.exceptions:
            ssn.debug(f'{exception.grade.name}: {exception.type.name}.\n' +
                      f'{exception.supplement}')
        if render_result.verdict == ErrorGrade.ERROR:
            ssn.print('Не можем отобразить текст вследствие ошибок рендера.')
        else:
            ssn.print(text)

        SessionCtl.halt(ssn)

    @classmethod
    async def new_text(cls, ssn: Session):
        ssn.print('Введите ID текста, по которому его будет легко найти:')
        id = await ssn.input()
        if len(id) == 0:
            ssn.print('Отменено!')
            SessionCtl.halt(ssn)
            return

        ssn.print('Введите шаблон текста:')
        text = ''
        while True:
            line = await ssn.input()
            if len(line) == 0:
                if len(text) == 0:
                    ssn.print('Отменено!')
                    break
                else:
                    render_result = cls.__renderer.check(text)
                    for exception in render_result.exceptions:
                        ssn.print(f'{exception.grade.name}: {exception.type.name}.\n' +
                                  f'{exception.supplement}')
                    if render_result.verdict == ErrorGrade.ERROR:
                        ssn.print('Текст не был добавлен вследствие ошибок.')
                    else:
                        cls.__textctl.insert(id, text)
                        ssn.print('Текст успешно добавлен!')
                    break
            else:
                text += line + '\n'
        SessionCtl.halt(ssn)

    @classmethod
    async def new_word(cls, ssn: Session):

        async def ask_form(word: str, path: tuple[str, ...] = ('')) -> str:
            ssn.print(', '.join((dir for dir in path)) + f' для слова "{word}":', end=' ')
            form = await ssn.input()
            return '+' if form == '' else form

        ssn.print('Введите слово:', end=' ')
        text = await ssn.input()
        if len(text) == 0:
            ssn.print('Отменено!')
            SessionCtl.halt(ssn)
            return

        tokens = text.split()
        word = tokens[0]
        tags = tokens[1:] if len(tokens) > 1 else []

        response = cls.__wordctl.check(word, tags)
        part_of_speech =\
            'глагол' if 'гл.' in response.tags else\
            'прилагательное/причастие' if 'пр.' in response.tags else\
            'существительное' if 'сущ.' in response.tags else\
            'указатель на слово' if any((re.match(r'&.', tag) for tag in response.tags)) else\
            'другое (наречие/деепричастие/...)'
        problem =\
            '!! ' if response.grade == ErrorGrade.ERROR else\
            '! ' if response.grade == ErrorGrade.WARNING else\
            ''
        problem +=\
            f'''
Нельзя ставить более одного указателя.
Есть конфликт тегов: {response.supplement}.
            ''' if response.status == WordDictStatus.REFERENCE_ALREADY_SET else\
            f'''
Тег \'{response.supplement}\' указывает на отсутствующее в словаре слово.
            ''' if response.status == WordDictStatus.INVALID_REFERENCE else\
            f'''
Это слово уже есть в списке.
Его теги: {response.supplement}.
            ''' if response.status == WordDictStatus.WORD_ALREADY_EXISTS else\
            f'''
Пожалуйста, укажите завершённость глагола: совершённый "сов." или несовершённый "несов."
            ''' if response.status == WordDictStatus.VERB_NO_PERFECTNESS else\
            f'''
Теги добавляются при вводе. Например, "любить гл. несов."; "человек сущ. м.р."
            ''' if response.status == WordDictStatus.NO_TAGS else\
            f'''
Вы не указали род существительного (м.р.|с.р.|ж.р.|безл.).
Выборка в тексте в основном требует род, что значит, ваше слово практически не будет показываться.
            ''' if response.status == WordDictStatus.NOUN_NO_GENDER else\
            f'''
Крайне не рекомендуем добавлять словосочетания.
            ''' if response.status == WordDictStatus.GOT_PHRASE else\
            f'''
Неизвестный статус "{response.status.name}".
Дополнительная информация: "{response.supplement}".
            ''' if response.status != WordDictStatus.OK else\
            ''

        ssn.print(f'''
Базовая форма слова: "{response.word}".
Часть речи: {part_of_speech}.
Теги: {response.tags}.
{problem}
                  ''')

        if response.grade != ErrorGrade.ERROR:
            ssn.print('Добавлять слово? (пустой ввод, если да)', end=' ')
            if len(await ssn.input()) == 0:
                await cls.__wordctl.insert(word, tags, ask_method=ask_form)
                ssn.print('Успешно добавлено!')
            else:
                ssn.print('Отменено!')

        SessionCtl.halt(ssn)

    @staticmethod
    async def help(ssn: Session, method: str = ''):
        if method != '':
            ssn.print(f'[{method}]\n  - {SessionCtl.details[method]}')
        else:
            for cmd, description in SessionCtl.details.items():
                ssn.print(f'[{cmd}]\n  - {description}')
        SessionCtl.halt(ssn)

    @classmethod
    async def main(cls, /, wordctl=WordDict, textctl=TextDict):
        cls.__wordctl = wordctl
        cls.__textctl = textctl
        cls.__renderer = Renderer(wordctl)

        SessionCtl.define_cmd([
            ('', AShell.help, 'Инструкция'),
            ('get_text', AShell.get_text, 'Печатает текст, основанный на случайном шаблоне'),
            ('new_text', AShell.new_text, 'Добавляет новый текстовый шаблон'),
            ('new_word', AShell.new_word, 'Добавляет новое слово в словарь'),
        ])
        SessionCtl.new('')

        while True:
            cmd: str = await aioconsole.ainput()
            if cmd.lower() in ('exit', 'quit', 'break'):
                break
            SessionCtl.input(cmd)

import random


class TextDict:

    def __init__(self, storage):
        self.__texts = storage('texts')

    def delete(self, *args):
        for id in args:
            del self.__texts[id]

    async def flush(self):
        await self.__texts.flush()

    async def save(self):
        await self.__texts.save()

    def get(self, id: str = '') -> str:
        if len(self.__texts) == 0:
            return ''
        if id == '':
            id = random.choice(list(self.__texts.keys()))
        return self.__texts[id]

    def insert(self, id: str, text: str):
        self.__texts[id] = text

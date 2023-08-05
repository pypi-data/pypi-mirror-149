import asyncio
from copy import copy
import os
from typing import Dict, Iterator, List, Union
import yaml

NestedDict = Dict[str, Union["NestedDict", str]]


class DbYaml():

    YAML_INDENT = 2

    def __init__(self, name: str):
        self.__filename = name + '.yaml'
        self.__inmem: NestedDict = dict()
        self.__cache: List[str] = list()

        if os.path.isfile(self.__filename):
            with open(self.__filename, mode='r', encoding='utf-8') as sin:
                saved = yaml.load(sin, yaml.Loader)
                if type(saved) == dict:
                    self.__inmem = saved

    def __setitem__(self, key: str, value: Union[NestedDict, str]):
        self.__inmem[key] = value
        self.__cache.append(key)

    def __getitem__(self, key: str) -> Union[NestedDict, str]:
        return self.__inmem[key]

    def __delitem__(self, key: str):
        if key in self.__cache:
            del self.__cache[key]
        del self.__inmem[key]

    def __iter__(self) -> Iterator[str]:
        return self.__inmem.__iter__()

    def __len__(self) -> int:
        return self.__inmem.__len__()

    def items(self):
        return self.__inmem.items()

    def keys(self):
        return self.__inmem.keys()

    async def flush(self):
        if len(self.__cache) != 0:
            with open(self.__filename, mode='a', encoding='utf-8') as sout:
                appendix = map(lambda word: (word, copy(self.__inmem[word])), self.__cache)
                await asyncio.to_thread(yaml.dump, dict(appendix), sout, indent=DbYaml.YAML_INDENT, allow_unicode=True)
            self.__cache.clear()

    async def save(self):
        if len(self.__inmem) != 0:
            with open(self.__filename, mode='w', encoding='utf-8') as sout:
                await asyncio.to_thread(yaml.dump, self.__inmem, sout, indent=DbYaml.YAML_INDENT, allow_unicode=True)

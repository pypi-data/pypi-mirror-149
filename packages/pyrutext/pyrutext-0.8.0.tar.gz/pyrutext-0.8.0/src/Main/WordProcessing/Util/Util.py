from contextlib import suppress
import re


def extract_any(self: list, *args, to_pop=False, if_none=None):
    for to_get in args:
        for from_list in self:
            if to_get == from_list:
                if to_pop:
                    self.remove(from_list)
                return to_get

    return if_none


def extract_all(self: list, *args, to_pop=False):
    to_return = []

    for to_get in args:
        for from_list in self:
            if to_get == from_list:
                if to_pop:
                    self.remove(from_list)
                to_return.append(to_get)

    return to_return


def safe_remove(self: list, elem):
    with suppress(ValueError, AttributeError):
        self.remove(elem)


def rel_format(self: str, mod: str):
    mod = re.sub(r'\+', self, mod)
    subtract_count = re.match(r'[\-]+', mod)
    subtract_count = 0 if subtract_count is None else len(subtract_count.group(0))
    return self[:-subtract_count] + mod[subtract_count:]

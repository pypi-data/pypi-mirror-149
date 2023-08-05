"""A Russian text generator based on templating texts and word picking"""

__version__ = "0.8.0"

import sys
import traceback
from Main.WordProcessing.WordDict import WordDict
from Main.TextProcessing.TextDict import TextDict
from StdIO.db_yaml import DbYaml as DB
from StdIO.io_ashell import AShell as IO
import asyncio


def main():
    word_manager = WordDict(DB)
    text_manager = TextDict(DB)

    try:
        asyncio.run(IO.main(wordctl=word_manager, textctl=text_manager))
    except KeyboardInterrupt:
        print('Плавно выходим из программы...')
    except Exception:
        traceback.print_exc(file=sys.stderr)
    finally:
        loop = asyncio.new_event_loop()
        loop.run_until_complete(word_manager.save())
        loop.run_until_complete(text_manager.save())
    sys.exit(0)


if __name__ == '__main__':
    main()

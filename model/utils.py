import datetime
from random import randint, choice, randrange
import re
import data.constants as c


def get_random_date(start, end):
    """Generate a random datetime between `start` and `end`"""
    return start + datetime.timedelta(
        # Get a random amount of seconds between `start` and `end`
        seconds=randint(0, int((end - start).total_seconds())),
    )


def get_random_word(alphabet: str, length: int):
    """Generate a random word on alphabet with given length"""
    return ''.join([choice(alphabet) for i in range(length)])


def get_random_email(alphabet: str):
    """Generate random email using function get_random_word(alphabet, length)"""
    return get_random_word(alphabet, randint(3, 10)) + '@' + get_random_word(alphabet, randint(2, 10)) + '.ru'


def random_string(prefix: str, max_length: int):
    return prefix+"".join([choice(c.SYMBOLS) for x in range(randrange(max_length))])


def clear(string):
    return re.sub("[() -/]", "", string)


def xstr(string):
    if string is None:
        return ""
    return str(string)


def remove_spaces(string):
    return ' '.join(xstr(string).strip().split())

import re
import requests


def _iter_names():
    response = requests.get('https://pypi.org/simple/')
    links = re.findall(r'href="(.+?)"', response.text)
    for link in links:
        yield link.removeprefix('/simple/').removesuffix('/')


def names() -> [str]:
    """
    Return all package names from pypi.org using the simple index
    """
    return list(_iter_names())

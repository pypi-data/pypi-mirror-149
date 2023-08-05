#!/usr/bin/env python
"""
Downloads chromedriver.
"""
import os
import platform
import re
import stat
import subprocess
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
from typing import IO

from xml.etree import ElementTree
from zipfile import ZipFile

import requests

import structlog

from hukudo.exc import HukudoException

logger = structlog.get_logger()

ARCHITECTURES = ['linux64', 'mac64', 'mac64_m1', 'win32']
# LHS: https://docs.python.org/3/library/platform.html#platform.system
# No Mac M2 :>
PLATFORM2ARCH = {
    'Linux': 'linux64',
    'Darwin': 'mac64',
    'Windows': 'win32',
}

try:
    cache_dir = os.environ['REQUESTS_CACHE_DIR']
    import requests_cache

    requests_cache.install_cache(cache_dir)
except KeyError:
    pass
except ModuleNotFoundError:
    logger.error('REQUESTS_CACHE_DIR set, but requests-cache not installed. Try: `pip install requests-cache`')
    raise


class ParseError(HukudoException):
    pass


class UnknownPlatformError(HukudoException):
    pass


class ChromedriverDownloadError(HukudoException):
    pass


@dataclass
class Version:
    version: str
    tuple: tuple[int]
    major: int
    url: str = None

    @classmethod
    def parse(cls, version):
        t = tuple(int(x) for x in version.split('.'))
        return cls(
            version=version,
            tuple=t,
            major=t[0],
        )

    def __lt__(self, other):
        return self.tuple < other.tuple

    def __str__(self):
        return self.version


def my_chrome_version(exe='google-chrome') -> Version:
    out = subprocess.check_output([exe, '--version'], encoding='utf-8')  # e.g. 'Google Chrome 100.0.4896.127 \n'
    m = re.match(r'.*?([\d.]+).*?', out)
    if m is None:
        raise ParseError(f'Could not parse version from "{out}"')
    return Version.parse(m.group(1))


def my_arch():
    x = platform.system()
    try:
        return PLATFORM2ARCH[x]
    except KeyError:
        raise UnknownPlatformError(x)


class ChromedriverRepo:
    def __init__(self, arch, url='https://chromedriver.storage.googleapis.com/'):
        if arch not in ARCHITECTURES:
            raise ValueError(f'Invalid architecture {arch}')
        self.arch = arch

        self.url = url

        response = requests.get(url)  # RAII
        response.raise_for_status()

        # strip default namespace https://stackoverflow.com/a/35165997/241240
        xml = re.sub(r"""\sxmlns=["'].+?["']""", '', response.text, count=1)
        self.root = ElementTree.fromstring(xml)

    def versions(self):
        """
        Find versions for given architecture. See ARCHITECTURES for valid values.
        """
        versions = []
        for e in self.root.findall('./Contents/Key'):
            key = e.text  # e.g. "99.0.4844.17/chromedriver_linux64.zip"
            match = re.match(fr'^([\d.]+)/chromedriver_{self.arch}.zip', key)
            if match:
                v = Version.parse(match.group(1))
                v.url = self.url + key
                versions.append(v)
        versions = sorted(versions)

        return versions

    def latest_version(self, major) -> Version:
        all_versions = self.versions()
        hits = sorted(v for v in all_versions if v.major == major)
        return hits[-1]


def download_zip(version: Version) -> IO[bytes]:
    log = logger.bind(version=version)
    log.info('downloading', url=version.url)
    response = requests.get(version.url)
    response.raise_for_status()
    zipfile = ZipFile(BytesIO(response.content))
    return zipfile.open('chromedriver')


def download_latest(target_dir: Path) -> [Version, Path]:
    if not target_dir.is_dir():
        raise ChromedriverDownloadError(f'not a directory: {target_dir}')

    arch = my_arch()
    repo = ChromedriverRepo(arch)
    chromedriver_version = repo.latest_version(my_chrome_version().major)

    target = target_dir / f'chromedriver-{chromedriver_version}'
    if target.exists():
        raise FileExistsError(target)

    fd = download_zip(chromedriver_version)
    target.write_bytes(fd.read())
    target.chmod(target.stat().st_mode | stat.S_IXUSR)
    return chromedriver_version, target

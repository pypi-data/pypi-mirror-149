import subprocess

import pytest


@pytest.mark.integration
def test_download(tmp_path):
    from hukudo.chromedriver import download_latest

    version, binary_path = download_latest(tmp_path)
    output = subprocess.check_output([str(binary_path), '--version'], encoding='utf-8')
    assert 'ChromeDriver' in output
    assert str(version) in output


@pytest.mark.integration
def test_lookup():
    from hukudo.chromedriver import ChromedriverRepo

    repo = ChromedriverRepo('linux64')
    versions = repo.versions()
    assert len(versions) > 0
    lv = repo.latest_version(100)
    assert lv.version.startswith('100.')


def test_my_chrome():
    from hukudo.chromedriver import my_chrome_version

    v = my_chrome_version()
    assert v.version
    assert v.major > 90

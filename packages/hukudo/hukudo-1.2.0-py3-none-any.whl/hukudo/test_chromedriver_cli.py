import pytest
from click.testing import CliRunner

from hukudo.cli import chromedriver


@pytest.mark.integration
def test_download(pytester):
    pytester.chdir()
    runner = CliRunner()
    # noinspection PyTypeChecker
    result = runner.invoke(chromedriver, ['download'])
    assert result.exit_code == 0
    path = next(pytester.path.glob('chromedriver-*'))
    assert path.is_file()
    x = path.stat()
    assert x.st_size > 0

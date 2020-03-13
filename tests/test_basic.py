from click.testing import CliRunner
from self.main import agilfy
import requests

def test_agilfy_success(requests_mock):
    requests_mock.get('https://api.agify.io/?name=Peter', text='{"age": 101}')
    runner = CliRunner()
    result = runner.invoke(agilfy, ['Peter'])
    assert result.exit_code == 0
    assert "lifespan is estimated to be: 101" in result.output

def test_agilfy_no_result(requests_mock):
    requests_mock.get('https://api.agify.io/?name=Peter', text='{"age": null}')
    runner = CliRunner()
    result = runner.invoke(agilfy, ['Peter'])
    assert result.exit_code == 0
    assert "hasn't been seen before" in result.output

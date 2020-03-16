from click.testing import CliRunner
from self.main import agilfy, pokemon, geoip, whois
from self import main
import requests
import os

'''
Agility tests
'''
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

def test_agilfy_timeout(requests_mock):
    requests_mock.get('https://api.agify.io/?name=Peter', exc=requests.exceptions.ConnectTimeout)
    runner = CliRunner()
    result = runner.invoke(agilfy, ['Peter'])
    assert result.exit_code == 1
    assert "Agilfy endpoint lookup failed" in result.output


'''
Pokemon tests
'''
def test_pokemon_success(requests_mock, testdir):
    pokemon_text = '''
    {
        "types": [
            {
                "type": 
                    {"name": "normal"}
            }
        ],
        "abilities": [
            {
                "ability": 
                    {"name": "imposter"}
            }
        ]

    }
    '''
    requests_mock.get('https://pokeapi.co/api/v2/pokemon/ditto', text=pokemon_text)
    runner = CliRunner()
    test_file = os.path.join(testdir, 'testdata/pokemon_input.txt')
    result = runner.invoke(pokemon, [test_file])
    assert result.exit_code == 0
    assert "Types: normal" in result.output
    assert "Abilities: imposter" in result.output

def test_pokemon_timeout(requests_mock, testdir):
    requests_mock.get('https://pokeapi.co/api/v2/pokemon/ditto', exc=requests.exceptions.ConnectTimeout)
    runner = CliRunner()
    test_file = os.path.join(testdir, 'testdata/pokemon_input.txt')
    result = runner.invoke(pokemon, [test_file])
    assert result.exit_code == 1
    assert "Pokeapi endpoint lookup failed" in result.output


'''
IP tests
'''
def test_ip_geoip_success(requests_mock):
    geoip_text = '''
    {
        "ip": {
            "country": "US",
            "continent": "NA",
            "region": "Michigan",
            "city": "Ann Arbor"
        }
    }
    '''
    requests_mock.get('https://api.apility.net/geoip/107.137.171.98', text=geoip_text)
    runner = CliRunner()
    result = runner.invoke(geoip, ['107.137.171.98'])
    assert result.exit_code == 0
    assert "Country: US" in result.output
    assert "Continent: NA" in result.output
    assert "Region: Michigan" in result.output
    assert "City: Ann Arbor" in result.output

def test_ip_geoip_timeout(requests_mock):
    requests_mock.get('https://api.apility.net/geoip/107.137.171.98', exc=requests.exceptions.ConnectTimeout)
    runner = CliRunner()
    result = runner.invoke(geoip, ['107.137.171.98'])
    assert result.exit_code == 1
    assert "Apility geoip endpoint lookup failed" in result.output

def test_ip_whois_success(mocker):
    whois_ret = {
        "nets": [
            {
                "name": "SIS-80-10-10-13",
                "handle": "NET-107-128-0-0-1",
                "created": "2013-10-23",
                "cidr": "107.128.0.0/12",
                "description": "AT&T Corp."
            }
        ]
    }
    # Whois does a bunch of stuff, easier just to mock out the lookup function
    mocker.patch.object(main, 'whois_lookup') 
    main.whois_lookup.return_value = whois_ret
    runner = CliRunner()
    result = runner.invoke(whois, ['107.137.171.98'])
    assert result.exit_code == 0
    assert "Name: SIS-80-10-10-13" in result.output
    assert "Handle: NET-107-128-0-0-1" in result.output
    assert "Registration Date: 2013-10-23" in result.output
    assert "CIDR: 107.128.0.0/12" in result.output
    assert "Organization: AT&T Corp." in result.output


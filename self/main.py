import click
import requests
from requests.exceptions import HTTPError
from ipwhois import IPWhois

def getOrNA(record, key):
    return record.get(key, "N/A")

def getJsonForRequest(url):
    try:
        response = requests.get(url, headers={'Accept': 'application/json'})
        response.raise_for_status()
    except:
        raise
    else:
        return response.json()

@click.group()
def main():
    print("Self-updating, multi-endpoint test project")

@main.command()
@click.argument("name")
def agilfy(name):
    try:
        ageJson = getJsonForRequest(f"https://api.agify.io?name={name}")
        age = ageJson['age']
        if age:
            print(f"{name}'s lifespan is estimated to be: {ageJson['age']}")
        else:
            print(f"{name} hasn't been seen before - no guess at the age!")

    except Exception as err:
        print(f"Agilfy endpoint lookup failed: {err}")

@main.command()
@click.argument("name")
def pokemon(name):
    try:
        pokemonJson = getJsonForRequest(f"https://pokeapi.co/api/v2/pokemon/{name}")
        print(f"Pokemon: {name}")
        print(f"Types: {', '.join([pokemonType['type']['name'] for pokemonType in pokemonJson['types']])}")
        print(f"Abilities: {', '.join([pokemonType['ability']['name'] for pokemonType in pokemonJson['abilities']])}")
    except Exception as err:
        print(f"Pokeapi endpoint lookup failed: {err}")

@main.group()
def ip():
    print("Querying various IP APIs...")

@ip.command()
@click.argument("ip")
def geoip(ip):
    try:
        geoipJson = getJsonForRequest(f"https://api.apility.net/geoip/{ip}")
        if 'ip' in geoipJson:
            ipRec = geoipJson['ip']
            print(f"IP: {ip}")
            print(f"Country: {getOrNA(ipRec, 'country')}")
            print(f"Continent: {getOrNA(ipRec, 'continent')}")
            print(f"Region: {getOrNA(ipRec, 'region')}")
            print(f"City: {getOrNA(ipRec, 'city')}")
        else:
            print("No geoip record.")
    except Exception as err:
        print(f"Apility geoip endpoint lookup failed: {err}")

@ip.command()
@click.argument("ip")
def whois(ip):
    try:
        wi = IPWhois(ip)
        rec = wi.lookup_whois()
        if len(rec['nets']) > 0:
            firstRec = rec['nets'][0]
            print(f"Name: {getOrNA(firstRec,'name')}")
            print(f"Handle: {getOrNA(firstRec,'handle')}")
            print(f"Registration Date: {getOrNA(firstRec,'created')}")
            print(f"CIDR: {getOrNA(firstRec,'created')}")
            print(f"Organization: {getOrNA(firstRec,'description')}")
        else:
            print("No whois record.")
    except Exception as err:
        print(f"Whois lookup failed: {err}")
  
if __name__ == '__main__':
    main()

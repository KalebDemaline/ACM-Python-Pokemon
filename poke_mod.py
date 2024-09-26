import requests
from multiset import *
import json 
import math
import pandas as pd
import concurrent.futures

def apiCall(paramString):
    url = f'https://pokeapi.co/api/v2/{paramString}'

    print('accessing url:', url)

    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json() 
        return {}
        
    except requests.exceptions.RequestException as e:
        # Handle any network-related errors or exceptions
        return {}

def fetchPokemonData(i, getPokemon, getSpecies, simpleMoves, simpleFlavorText):
    pokeObj = {}

    # make API call to pokemon endpoint
    if getPokemon:
        pokeObj.update(apiCall(f'pokemon/{i}'))
        if simpleMoves:
            newMoves = []
            if 'moves' in pokeObj:
                for m in pokeObj['moves']:
                    newMoves.append({'move': m['move'], 'version_group_details': []})
            pokeObj['moves'] = newMoves

    # make API call to species endpoint 
    if getSpecies:
        pokeObj.update(apiCall(f'pokemon-species/{i}'))
        if simpleFlavorText:
            newFlavorText = []
            if 'flavor_text_entries' in pokeObj:
                for f in pokeObj['flavor_text_entries']:
                    newFlavorText.append({'flavor_text': f['flavor_text']})
            pokeObj['flavor_text_entries'] = newFlavorText

    return pokeObj

# Access a list of pokemon from the Pokedex API, using json cache files if indicated 
# Makes a request for a pokemon and/or species for every id from 1 to count
def loadPokemon(
        count, # number of pokemon to load
        updateCache=False, # if True, update the corresponding json cache file in json-cache/
        loadFromCache=False, # if True, retrieve all requested information from a json cache. Make API calls for non-cached info
        getPokemon=True, getSpecies=True, # determine which endpoints to access: pokemon/ and pokemon-species/
        simpleMoves=True, simpleFlavorText=True # if True, remove large amounts of extra information from moves and flavor_text_entries
        ):
    
    # determine which file to use for cache
    cacheFileName = ''
    if (getPokemon):
        cacheFileName += 'Pokemon'
    if (getSpecies):
        cacheFileName += 'Species'
    
    pokeList = []
    cachedPokeList = []

    # load data from a json cache file 
    if (loadFromCache):
        try:
            with open(f'json-cache/{cacheFileName}.json', 'r') as read_file:
                cachedPokeList = json.load(read_file)
        except:
            cachedPokeList = []

    #create a set of id's already accessed from cache
    idsFound = {}
    for p in cachedPokeList:
        idsFound[p['id']] = p

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(fetchPokemonData, i, getPokemon, getSpecies, simpleMoves, simpleFlavorText): i for i in range(1, count + 1) if i not in idsFound}
        for future in concurrent.futures.as_completed(futures):
            i = futures[future]
            try:
                pokeObj = future.result()
                pokeObj['id'] = i
                pokeList.append(pokeObj)
            except Exception as e:
                print(f'Error fetching data for Pokemon ID {i}: {e}')
    
    # Add cached Pokemon to the list
    for i in range(1, count + 1):
        if i in idsFound:
            pokeList.append(idsFound[i])

    # output data to a json cache file 
    if updateCache:
        with open(f'json-cache/{cacheFileName}.json', 'w') as write_file:
            json.dump(pokeList, write_file, indent=4)

    return pokeList


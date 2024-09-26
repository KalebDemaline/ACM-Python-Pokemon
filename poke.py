from poke_mod import *
import numpy as np
import matplotlib.pyplot as plt 

loadPokemon(1025, True, False, True, False)

weightDict = {}
letterCount = {}

with open ('json-cache/PokemonSpecies.json', 'r') as f:
    loadedJson = json.load(f)

for pokemon in loadedJson: 
    if pokemon['name'][0] in weightDict.keys():
        weightDict[pokemon['name'][0]] += pokemon['weight']
        letterCount[pokemon['name'][0]] += 1
    else:
        weightDict[pokemon['name'][0]] = pokemon['weight']
        letterCount[pokemon['name'][0]] = 1

weightDict = dict(sorted(weightDict.items()))
letterCount = dict(sorted(letterCount.items()))

averageWeight = {letter : weightDict[letter]/letterCount[letter] for letter in letterCount.keys()}

letters = list(averageWeight.keys())
avgWeight = list(averageWeight.values())
count = list(letterCount.values())

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(24, 8))

# First subplot: Average Weight
ax1.bar(letters, avgWeight, color='maroon', width=0.6)
ax1.set_xlabel("Start letter")
ax1.set_ylabel("Average Weight")
ax1.set_title("Average weight based on first letter of name")

# Second subplot: Count
ax2.bar(letters, count, color='teal', width=0.6)
ax2.set_xlabel("Start letter")
ax2.set_ylabel("Count")
ax2.set_title("# of pokemon with start letter")

plt.tight_layout()
plt.show()
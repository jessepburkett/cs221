## import required data from Kaggle datasets
import numpy as np
import pandas as pd
import ast


def get_move_data():
	moves = pd.read_csv('move-data.csv', index_col = 0)
	## convert csv vals for Move power and accuracy to floats (or nan)
	for var in ['Power', 'Accuracy']:
		moves[var].replace('None', np.nan, inplace=True)
		moves[var] = moves[var].astype(float)

	## convert from data frame to dict of move-->(type, category, pp, power, accuracy)
	movesDict = moves.to_dict()
	nameDict = {}
	for key in movesDict['Name']:
		nameDict[movesDict['Name'][key].lower()] = [movesDict['Type'][key], movesDict['Category'][key], movesDict['PP'][key], movesDict['Power'][key], movesDict['Accuracy'][key]]
	return nameDict

def get_pokemon_data():
	pokemon = pd.read_csv('pokemon-data.csv', sep = ';', converters={'Types':ast.literal_eval, 'Abilities':ast.literal_eval, 'Moves':ast.literal_eval})

	## convert from data frame to dict of pokemon name-->[type, category, pp, power, accuracy]
	pokeDict = pokemon.to_dict()
	pokeNameDict = {}
	for key in pokeDict['Name']:
		pokeNameDict[pokeDict['Name'][key].lower()] = [pokeDict['Types'][key], pokeDict['Abilities'][key], [pokeDict['HP'][key], pokeDict['Attack'][key], pokeDict['Defense'][key], pokeDict['Special Attack'][key], pokeDict['Special Defense'][key], pokeDict['Speed'][key]], pokeDict['Moves'][key]]
	return pokeNameDict
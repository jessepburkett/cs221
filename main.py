## implement user input stream
import data_loader
import pokemon

#TEAM_SIZE = 2

def get_team_size():
	teamSize = 0
	while True:
		try:
			teamSize = int(input("Please enter your team size (must be between 1 and 6): "))
		except ValueError:
			print("Sorry, that's not a valid number.")
			#better try again... Return to the start of the loop
			continue
		else:
			#age was successfully parsed!
			#we're ready to exit the loop.
			if teamSize > 0 and teamSize <= 6:
				return teamSize
			else:
				print('Teams must between 1 and 6 Pokemon')
				continue

def add_pokes(teamSpots, pokeDict):
	Player1 = []

	while True:

		inputStr = input("Enter a pokemon's name or QUIT to quit: ").lower()
		if (inputStr == 'quit') or (inputStr == 'q'):
			return Player1
			break
		else:
			if inputStr in pokeDict:
				if teamSpots - 1 > 0:
					print("You added %s to your team! You have %d spots remaining on your team." % (inputStr, teamSpots - 1))
					teamSpots -= 1
					Player1.append(pokemon.Pokemon(pokeDict, inputStr))
				else:
					teamSpots -= 1
					Player1.append(pokemon.Pokemon(pokeDict, inputStr))
					print("Your team is full, let's take a look: ")
					for poke in Player1:
						print([poke.name, poke.types, poke.ability, poke.stats, poke.moves])
					return Player1
					break
			else: print("That doesn't seem to be a Pokemon, make sure you spelled it correctly. Or press \'q\' to exit")
	return

def main():
	print("Loading Pokemon Data...")

	## Creates a Dictionary of move name-->[type, category, pp, power, accuracy]
	movesDict = data_loader.get_move_data()

	## Creates a Dictionary of pokemon name-->[type, category, pp, power, accuracy]
	pokeDict = data_loader.get_pokemon_data()

	## dictate team size
	teamSpots = get_team_size()

	## create list of Pokemon objects to create a team
	Team1 = add_pokes(teamSpots, pokeDict)

	quit()

if __name__ == '__main__':
	main()
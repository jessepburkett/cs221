#Type effectiveness as a sparse dict
# atkType-->{defType-->float(damage amplifier)}
effectiveness = {
	'normal':{'rock':0.5, 'ghost':0.0}
	'fire':{'rock':0.5, 'fire':0.5, 'water':0.5, 'grass':2.0, 'ice':2.0, 'bug':2.0, 'dragon':0.5}
	'water':{'fire':2.0, 'water':0.5, 'grass':0.5, 'ground':2.0, 'rock':2.0, 'dragon':0.5}
	'electric':{'water':2.0, 'electric':0.5, 'grass':0.5, 'ground':0.0, 'flying':2.0, 'dragon':0.5}
	'grass':{'fire':0.5, 'water':2.0, 'grass':0.5, 'poison':0.5, 'ground':2.0, 'flying':0.5, 'bug':0.5, 'rock':2.0, 'dragon':0.5}
	'ice':{'water':0.5, 'grass':2.0, 'ice':0.5, 'ground':2.0, 'flying':2.0, 'dragon':2.0}
	'fighting':{'normal':2.0, 'ice':2.0, 'poison':0.5, 'flying':0.5, 'psychic':0.5, 'bug':0.5, 'rock':2.0, 'ghost':0.0}
	'poison':{'grass':2.0, 'poison':0.5, 'ground':0.5, 'bug':2.0, 'rock':0.5, 'ghost':0.5}
	'ground':{'fire':2.0, 'electric':2.0, 'grass':0.5, 'poison':2.0, 'flying':0.0, 'bug':0.5, 'rock':2.0}
	'flying':{'electric':0.5, 'grass':2.0, 'fighting':2.0, 'bug':2.0, 'rock':0.5}
	'psychic':{'fighting':2.0, 'poison':2.0, 'psychic':0.5}
	'bug':{'fire':0.5, 'grass':2.0, 'fighting':0.5, 'poison':2.0, 'flying':0.5, 'psychic':2.0}
	'rock':{'fire':2.0, 'ice':2.0, 'fighting':0.5, 'ground':0.5, 'flying':2.0, 'bug':2.0}
	'ghost':{'normal':0.0, 'psychic':0.0, 'ghost':2.0}
	'dragon':{'dragon':2.0}
}

def getDmgMult(moveType, defType):
	mult = 1
	if defType[0] in effectiveness[moveType]:
		mult *= effectiveness[moveType][defType[0]]
	if defType[1] is not None and defType[1] in effectiveness[moveType]:
		mult *= effectiveness[moveType][defType[1]]
	return mult


def damageCalc(self, index, move):
        if index == 1:
            power = self.agent['Pokemon'][self.currAgent]['moves'][move][0]
            moveType = self.agent['Pokemon'][self.currAgent]['moves'][move][2]
            
            atkType = self.agent['Pokemon'][self.currAgent]['type']
            atk = self.agent['Pokemon'][self.currAgent]['stats']['atk'] if moveType == 'physical' else self.agent['Pokemon'][self.currAgent]['stats']['spc']
            
            defType = self.opp['Pokemon'][self.currOpp]['type']
            defense = self.opp['Pokemon'][self.currOpp]['stats']['def'] if moveType == 'physical' else self.opp['Pokemon'][self.currOpp]['stats']['spc']
        else:
            power = self.opp['Pokemon'][self.currOpp]['moves'][move][0]
            moveType = self.opp['Pokemon'][self.currOpp]['moves'][move][2]

            atkType = self.opp['Pokemon'][self.currOpp]['type']
            atk = self.opp['Pokemon'][self.currOpp]['stats']['atk'] if moveType == 'physical' else self.opp['Pokemon'][self.currOpp]['stats']['spc']
            
            defType = self.agent['Pokemon'][self.currAgent]['type']
            defense = self.agent['Pokemon'][self.currAgent]['stats']['def'] if moveType == 'physical' else self.agent['Pokemon'][self.currAgent]['stats']['spc']

        stab = 1.5 if moveType == atkType[0] or moveType == atkType[1] else 1
        dmgMult = getDmgMult(moveType, defType)

        damage = ((((2 * LEVEL)/5 + 2) * power * atk / defense)/50 + 2) * stab * dmgMult
        return math.floor(damage)
## implement the Pokemon class

class Pokemon(object):
	"""docstring for Pokemon"""
	def __init__(self, data, name):
		super(Pokemon, self).__init__()
		self.data = data
		self.name = name
		self.types = data[name][0]
		self.stats = data[name][2]
		self.ability = data[name][1][0]	## just choosing the first possible ability for now
		self.moves = [data[name][3][0], data[name][3][1], data[name][3][2], data[name][3][3]]	## choose the pokemon's first possible four moves for now
		self.status = None
		
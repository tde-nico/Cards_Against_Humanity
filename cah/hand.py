
class Hand:
	MAX_CARDS = 10

	def __init__(self, name, db):
		self.name = name
		self.db = db
		self.cards = []
		self.awesome_points = 0
		self.draw()

	def draw(self):
		while len(self.cards) < self.MAX_CARDS:
			card = self.db.draw('white')
			#print(card)
			self.cards.append(card)

	def pick(self, index):
		card = None
		if self.cards:
			card = self.cards.pop(index)
		return card

	def get_hand(self):
		return self.cards

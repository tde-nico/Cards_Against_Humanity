import json
import random


def load(fname):
	data = None
	with open(fname, mode='r', encoding='utf-8') as f:
		data = json.load(f)
	return data


class DB:
	def __init__(self, fname):
		self.all_cards = load(fname)
		self.load_cards()

	def load_cards(self):
		self.white_cards = []
		self.black_cards = []
		for sets in self.all_cards:
			if sets['white']:
				self.white_cards.append({'name': sets['name'], 'cards': sets['white']})
			if sets['black']:
				self.black_cards.append({'name': sets['name'], 'cards': sets['black']})

	def draw(self, color):
		if color == 'white':
			current_set = self.white_cards
		else:
			current_set = self.black_cards
		if not current_set:
			return
		cars_sets_num = len(current_set)
		card_set = random.randint(0, cars_sets_num - 1)
		cards_num = len(current_set[card_set]['cards'])
		#print(cards_num, card_set)
		selected_card = random.randint(0, cards_num - 1)
		card = current_set[card_set]['cards'].pop(selected_card)
		if not current_set[card_set]['cards']:
			current_set.pop(card_set)
		return card

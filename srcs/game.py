from .settings import *
from kivymd.uix.card import MDCard
from kivy.properties import StringProperty
from kivy.clock import mainthread
from time import sleep
import random
import threading


class MD3Card(MDCard):
	#text = StringProperty()

	def set_attributes(self, game, color):
		self.game = game
		self.card_color = color

	def on_press(self):
		if self.card_color == 'black':
			return
		self.game.set_card_selection(self)
		#print(self.ids['card_label'].text)
		return super().on_press()


class Game:
	def __init__(self, app):
		self.app = app
		self.cah = self.app.cah


	def set_defaults(self):
		self.md_cards = []
		self.selected_cards = []
		self.evaluation_cards = []
		self.czar = None
		self.host = None
		self.app.root.ids[f'card_list_{self.mode}'].clear_widgets()
		if self.mode == 'player':
			self.app.root.ids['player_label'].text = 'Waiting Room'
		elif self.mode == 'host':
			self.app.root.ids['host_label'].text = ''


	def open(self, mode):
		self.mode = self.cah.mode = mode
		self.set_defaults()
		if mode == 'player':
			self.cah.join()
			self.waiting_room = threading.Thread(target=self.start_game)
			self.waiting_room.start()
		elif mode == 'host':
			self.cah.join('host')
		self.app.root.ids['screen_manager'].current = f"game_{self.mode}"


	@mainthread
	def leave(self):
		self.cah.stop_client()
		self.set_defaults()
		self.app.root.ids['screen_manager'].current = "home"
	

	def shut(self):
		if self.cah.client:
			self.cah.client.send({'message': 'leave'})
		self.leave()
		self.cah.stop_server()
	

	def list_rooms(self):
		text = self.cah.list_rooms()
		self.app.root.ids['host_label'].text = text


	@mainthread
	def generate_cards(self):
		for card in self.cah.player.get_hand():
			mdcard = MD3Card(
				line_color=(0.2, 0.2, 0.2, 0.8),
				style="filled",
				padding="4dp",
				size_hint=(None, None),
				size=("200dp", "100dp"),
				md_bg_color="#eeeeee",
			)
			mdcard.ids['card_label'].text = card['text']
			mdcard.set_attributes(self, 'white')
			self.md_cards.append(mdcard)
			self.app.root.ids[f'card_list_{self.mode}'].add_widget(mdcard)

		mdcard = MD3Card(
			line_color=(0.2, 0.2, 0.2, 0.8),
			style="filled",
			padding="4dp",
			size_hint=(None, None),
			size=("200dp", "100dp"),
			md_bg_color="#222222",
		)
		mdcard.ids['card_label'].text = self.black_card['text']
		mdcard.ids['card_label'].color = 'white'
		mdcard.set_attributes(self, 'black')
		self.app.root.ids[f'black_card_{self.mode}'].add_widget(mdcard)


	def start_hosted_game(self):
		self.starter_thread = threading.Thread(target=self.start_game)
		self.starter_thread.start()


	def start_game(self):
		while not self.cah.player:
			sleep(0.1)
		if self.mode == 'host':
			self.set_czar()
			self.host = self.cah.client.identifier
		elif self.mode == 'player':
			waiting = None
			while not waiting:
				if self.cah.client:
					waiting = self.cah.client.get_messages()
				else:
					return
				sleep(0.1)
			#print(waiting)
			message = json.loads(waiting.pop())
			sender, value = message.popitem()
			if value.get('message', None) == 'leave':
				self.leave()
				return
			self.czar, self.black_card = value['czar'], value['card']
			self.host = sender
			self.app.root.ids['player_label'].text = ''
		self.generate_cards()
		#if self.mode == 'player':
		self.wait_commands()


	def wait_commands(self):
		while self.cah.client:
			waiting = None
			while not waiting:
				if self.cah.client:
					waiting = self.cah.client.get_messages()
				else:
					return
				sleep(0.1)
			message = json.loads(waiting.pop())
			sender, value = message.popitem()
			if sender == self.host:
				if value['message'] == 'leave':
					self.leave()
			elif self.cah.client.identifier == self.host:
				if value['message'] == 'selection':
					self.evaluation_cards.append([value['cards'], value['identifier']])
					print(list(self.cah.rooms.rooms.items())[0][1].players, self.evaluation_cards)
					if len(self.evaluation_cards) == len(list(self.cah.rooms.rooms.items())[0][1].players) - 1:
						print('selection')


	def set_czar(self):
		self.czar = random.choice(list(self.cah.rooms.players.keys()))
		self.black_card = self.cah.db.draw('black')
		self.cah.client.send({'czar': self.czar, 'card': self.black_card})


	def select_cards(self):
		if len(self.selected_cards) != self.black_card['pick']:
			return
		if self.cah.client.identifier != self.host:
			#print(self.host, self.czar)
			self.cah.client.sendto(self.host, {'cards': self.selected_cards,
				'identifier': self.cah.client.identifier, 'message': 'selection'})
		else:
			self.evaluation_cards.append([self.select_cards, self.cah.client.identifier])
		#print(self.black_card['pick'])
		#print(self.selected_cards)
		self.selected_cards = []


	def set_card_selection(self, mdcard):
		text = mdcard.ids['card_label'].text
		if text in self.selected_cards:
			self.selected_cards.remove(text)
			mdcard.md_bg_color = '#eeeeee'
		else:
			self.selected_cards.append(text)
			mdcard.md_bg_color = '#bbbbbb'


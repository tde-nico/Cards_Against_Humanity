from .settings import *
from kivymd.uix.card import MDCard
from kivy.properties import StringProperty
from kivy.clock import mainthread
from time import sleep
import random
import threading


class MD3Card(MDCard):
	text = StringProperty()

	def on_touch_up(self, touch):
		#self.md_bg_color = '#cccccc'
		pass


class Game:
	def __init__(self, app):
		self.app = app
		self.cah = self.app.cah


	def set_defaults(self):
		self.md_cards = []
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
			self.md_cards.append(mdcard)
			self.app.root.ids[f'card_list_{self.mode}'].add_widget(mdcard)


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
			print(waiting)
			message = json.loads(waiting.pop())
			sender, value = message.popitem()
			if value.get('message', None) == 'leave':
				self.leave()
				return
			self.czar = value['czar']
			self.host = sender
			self.app.root.ids['player_label'].text = ''
		self.generate_cards()
		if self.mode == 'player':
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


	def set_czar(self):
		self.czar = random.choice(list(self.cah.rooms.players.keys()))
		self.cah.client.send({'czar': self.czar})

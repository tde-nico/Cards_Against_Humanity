from .settings import *
from kivymd.uix.card import MDCard
from kivy.properties import StringProperty
from time import sleep


class MD3Card(MDCard):
	text = StringProperty()

	def on_touch_up(self, touch):
		#self.md_bg_color = '#cccccc'
		pass


class Game:
	def __init__(self, app):
		self.app = app
		self.cah = self.app.cah
		self.md_cards = []


	def open(self, mode):
		self.mode = self.cah.mode = mode
		if mode == 'player':
			self.cah.join()
		elif mode == 'host':
			self.cah.join('host')
		self.app.root.ids['screen_manager'].current = f"game_{self.mode}"
		while not self.cah.player:
			sleep(0.1)  # "filled": "#f4dedc"
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
			self.app.root.ids[f'card_list_{mode}'].add_widget(mdcard)


	def leave(self):
		self.cah.stop_client()
		self.md_cards = []
		self.app.root.ids['screen_manager'].current = "home"
	

	def shut(self):
		self.cah.stop_client()
		self.cah.stop_server()
		self.md_cards = []
		self.app.root.ids['screen_manager'].current = "home"
	

	def list_rooms(self):
		text = self.cah.list_rooms()
		self.app.root.ids['host_label'].text = text


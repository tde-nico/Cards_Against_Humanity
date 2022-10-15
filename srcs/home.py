from srcs.settings import *

class Home:
	def __init__(self, app):
		self.app = app


	def open(self):
		if self.app.cah.mode == 'player':
			self.app.root.ids['screen_manager'].current = "game_player"
		elif self.app.cah.mode == 'host':
			self.app.root.ids['screen_manager'].current = "game_host"
		else:
			self.app.root.ids['screen_manager'].current = "home"
		self.app.root.ids['nav_drawer'].set_state("close")

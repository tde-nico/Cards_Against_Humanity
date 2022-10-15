from .settings import *

class Game:
	def __init__(self, app):
		self.app = app


	def open(self, mode):
		self.mode = self.app.cah.mode = mode
		if mode == 'player':
			self.app.cah.join()
		elif mode == 'host':
			self.app.cah.join('host')
		self.app.root.ids['screen_manager'].current = f"game_{self.mode}"


	def leave(self):
		self.app.cah.stop_client()
		self.app.root.ids['screen_manager'].current = "home"
	

	def shut(self):
		self.app.cah.stop_client()
		self.app.cah.stop_server()
		self.app.root.ids['screen_manager'].current = "home"
	

	def list_rooms(self):
		self.app.cah.list_rooms()


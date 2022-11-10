from kaki.app import App
from kivymd.app import MDApp
from kivy.factory import Factory
import os

class MD_Hot_Reload(App, MDApp):


	DEBUG = 1

	CLASSES = {
		"main_app": "main"
	}

	KV_FILES = {
		os.path.join(os.getcwd(), "main_app.kv")
	}

	AUTORELOADER_PATHS = [
		(".", {"recursive": True})
	]

	def build_app(self):
		print("Started Hot Reload")
		return Factory.main_app()

MD_Hot_Reload().run()

# ($env:DEBUG=1) -and (py hot_reload.py)

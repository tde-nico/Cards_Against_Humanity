import kivy
import kivymd
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
#from kivy.lang import Builder
#from kivy.core.window import Window
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.menu import MDDropdownMenu

import os, json

kivy.require('2.0.0')

TITLE = "Card Against Humanity"
DEVELOPER = "tde-nico"
GIT = "https://github.com/tde-nico"
VERSION = "0.0.1"
SETTINGS_FILE = 'settings.json'
PORT = 1235

PLATFORM = kivy.utils.platform
SETTINGS = dict()

if PLATFORM == 'android':
	import android_api
	from android_api.notification import notify



def	dump(fname, data):
	with open(fname, 'w') as f:
		json.dump(data, f)

def load(fname):
	with open(fname, 'r') as f:
		data = json.load(f)
	return data

def debug(error):
	with open(SETTINGS['download'] + '/log.txt', 'w') as d:
		d.write(error)



# ssl permisson
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

if PLATFORM == 'android':
	# request permissions for android
	from android.permissions import request_permissions, Permission
	request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
	# storage permissions
	from android.storage import primary_external_storage_path
	common_dir = primary_external_storage_path()
	# default download folder
else:
	kivy.core.window.Window.size = (450, 700)
	common_dir = os.getcwd()
	common_dir = common_dir.replace("\\", "/")
	if not os.path.exists(common_dir + "/Download"):
		os.mkdir(common_dir + "/Download")



DEFAULTS = {
	'theme': 'Dark',
	'palette': 'Teal',
}


COLORS = ['Red','Pink','Purple','DeepPurple','Indigo','Blue','LightBlue','Cyan','Teal','Green',
			'LightGreen', 'Lime','Yellow','Amber','Orange','DeepOrange','Brown','Gray','BlueGray']



def reset_settings():
	#SETTINGS = DEFAULTS
	for key, item in DEFAULTS.items():
		SETTINGS[key] = item
	dump(SETTINGS_FILE, SETTINGS)

try:
	SETTINGS = load(SETTINGS_FILE)
except:
	reset_settings()


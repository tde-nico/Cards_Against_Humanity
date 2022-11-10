from srcs.settings import *


class Settings:
	def __init__(self, app):
		self.app = app
		self.manager_open = False
		self.dialog = None


	def open(self):
		try:
			debug("settings")
			if self.app.theme_cls.theme_style == 'Dark':
				self.app.root.ids['theme'].active = True
			self.app.root.ids['palette'].text = SETTINGS['palette']

			self.palette_menu = MDDropdownMenu(
				caller=self.app.root.ids.palette,
				items = [{
					"text": color,
					'viewclass': 'OneLineListItem',
					'on_release': lambda x=color: self.change_palette(x)
					} for color in COLORS],
				width_mult=2,
				max_height=700,
				position="bottom",
				)
			self.app.root.ids['screen_manager'].current = 'settings'
			self.app.root.ids['nav_drawer'].set_state("close")
		except Exception as e:
			debug(e)


	def change_theme(self):
		if self.app.root.ids['theme'].active:
			self.app.theme_cls.theme_style = "Dark"
			SETTINGS["theme"] = 'Dark'
		else:
			self.app.theme_cls.theme_style ="Light"
			SETTINGS["theme"] = 'Light'
		dump(SETTINGS_FILE, SETTINGS)


	def change_palette(self, palette):
		self.palette_menu.dismiss()
		self.app.theme_cls.primary_palette = palette
		self.app.root.ids['palette'].text = palette
		SETTINGS["palette"] = palette
		dump(SETTINGS_FILE, SETTINGS)


	def reset(self):
		if self.dialog == None:
			self.dialog = MDDialog(
				title="Reset settings?",
				text="This will reset your device to its default factory settings.",
				buttons=[
					MDFlatButton(
						text="CANCEL",
						theme_text_color="Custom",
						text_color=self.app.theme_cls.primary_color,
						on_press=self._not_reset,
					),
					MDFlatButton(
						text="CONTINUE",
						theme_text_color="Custom",
						text_color=self.app.theme_cls.primary_color,
						on_press=self._reset,
					),
				],
			)
		self.dialog.open()

	def _not_reset(self, *args):
		self.dialog.dismiss()

	def _reset(self, *args):
		self.dialog.dismiss()
		reset_settings()
		self.app.theme_cls.primary_palette = SETTINGS['palette']
		self.app.root.ids['palette'].text = SETTINGS['palette']
		self.app.theme_cls.theme_style = SETTINGS['theme']
		self.app.root.ids['theme'].active = True



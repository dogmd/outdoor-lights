import led_control.effects as effects
import json
import colorsys

class EffectController:
	def __init__(self, num_pixels):
		self.import_settings()
		self.pixels = []
		for i in range(num_pixels):
			self.pixels.append((0, 0, 0))
		self.time = 0

	def import_settings(self):
		self.effects = []
		with open('led_control/settings.json', 'r') as settings:
			data = settings.read()
		self.settings = json.loads(data)

		for effect_name, effect_settings in self.settings['effects'].items():
			if (bool(effect_settings['selected'])):
				self.effects.append((effects.lookup(effect_name), effect_settings))

		self.brightness = float(self.settings['powerSettings']['brightness']) / 100
		if (self.settings['powerSettings']['isOn'] == 'false'):
			self.brightness = 0

	def step(self):
		for effect in self.effects:
			effect[0](effect[1], self.time, self.pixels) # effect[0] is callback, effect[1] is effect settings
		self.apply_brightness()
		self.time += 1

	def apply_brightness(self):
		for i, color in enumerate(self.pixels):
			color = tuple(c / 255 for c in color)
			hls = colorsys.rgb_to_hls(*color)
			hls = (hls[0], hls[1] * self.brightness, hls[2])
			self.pixels[i] = tuple(c * 255 for c in colorsys.hls_to_rgb(*hls))
from food import Food

class Drinks(Food):
	def __init__(self, name, price, volume, type):
		super().__init__(name, price)
		self._volume = volume
		self._type = type

	@property
	def volume(self):
		return self._volume

	@volume.setter
	def volume(self, volume):
		self._volume = volume

	@property
	def type(self):
		return self._type

	@type.setter
	def type(self, type):
		self._type = type

	def __str__(self):
		
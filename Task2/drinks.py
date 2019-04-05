from food import Food

class Drinks(Food):
	def __init__(self, name, price, size):
		super().__init__(name, price)
		self._size = size

	@property
	def volume(self):
		return self._size

	@volume.setter
	def volume(self, volume):
		self._size = size

	def computePrice(self):
        	pass
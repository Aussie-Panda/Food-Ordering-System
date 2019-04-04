from food import Food

class Drinks(Food):
	def __init__(self, name, price, size, type):
		super().__init__(name, price)
		self._size = size
		self._type = type

	@property
	def volume(self):
		return self._size

	@volume.setter
	def volume(self, volume):
		self._size = size

	@property
	def type(self):
		return self._type

	@type.setter
	def type(self, type):
		self._type = type

	def computePrice(self):
        	pass

	def __str__(self):
		return "{}: {}ml {} for ${}".format(self.type, self.size, self.name, self.price)
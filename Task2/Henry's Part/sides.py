from food import Food

class Sides(Food):

	def __init__(self, name, price, size, type):
		super().__init__(name, price)
		self._size = size
		self._type = type

	@property
	def sizeOfSides(self):
		return self._size

	def size(self, size):
		self._size = size

	@property
	def sidesType(self):
		return self._type

	def type(self, type):
		self._type = type

	def computePrice(self):
        	pass
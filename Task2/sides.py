from food import Food

class Sides(Food):
	def __init__(self, name, price, size):
		super().__init__(name, price)
		self._size = size

	@property
	def size(self):
		return self._size

	@size.setter
	def size(self, size):
		self._size = size

	def computePrice(self):
        	pass

	def __str__(self):
		return "{}{}: ${}.format(self.size, self.name, self.price)"
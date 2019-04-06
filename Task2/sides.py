from food import Food

class Sides(Food):
	def __init__(self, name, price, size, volumn):
		super().__init__(name, price)
		self._size = size
		self._volumn = volumn 

	@property
	def size(self):
		return self._size

	@property
	def volumn(self):
		return self._volumn
	

	def computePrice(self):
        	pass

	def __str__(self):
		return f"{self.name}({self.size}): ${self.price}"
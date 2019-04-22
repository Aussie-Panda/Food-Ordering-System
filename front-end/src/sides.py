from src.food import Food

class Sides(Food):
	def __init__(self, name, price, size, volumn, unit):
		super().__init__(name, price)
		self._size = size
		self._volumn = volumn 
		self._unit = unit

	@property
	def size(self):
		return self._size

	@property
	def volumn(self):
		return self._volumn
	
	@property
	def unit(self):
		return self._unit
	

	def computePrice(self):
        	pass

	def __str__(self):
		return f"{self.name}({self.size}): ${self.price}"
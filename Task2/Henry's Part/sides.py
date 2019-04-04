from food import Food

class Sides(Food):
	def __init__(self, name, price, size, type):
		super().__init__(name, price)
		self._size = size
		self._type = type

	@property
	def size(self):
		return self._size

	@size.setter
	def size(self, size):
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
		return "{}: {} {} for ${}".format(self.type, self.size, self.name, self.price)

#x = Sides('fries', 2, 'large', 'Side')
#print(x)
#print(x.size)
#print(x.type)
#x.size = 'medium'
#print(x.size)
#x.type = 'Test'
#print(x.type)
#print(x)
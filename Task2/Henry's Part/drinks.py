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

	def computePrice(self):
        	pass

	def __str__(self):
		return "{}: {}ml {} for ${}".format(self.type, self.volume, self.name, self.price) 
		
#x = Drinks('can', 2, 375, 'Drink')
#print(x)
#print(x.volume)
#print(x.type)
#x.volume = 600
#print(x.volume)
#x.type = 'Test'
#print(x.type)
#print(x)
from food import Food

class Drinks(Food):
	def __init__(self, name, price, size, volumn):
		super().__init__(name, price)
		self._size = size
		self._volumn = volumn


	@property
	def volumn(self):
		return self._volumn

	@property
	def size(self):
		return self._size
	

	def computePrice(self):
		pass

	# output example: Lemonade(Bottles): $3
	def __str__(self):
		return f"{self.name}({self.size}:{self.volumn}ml): ${self.price}"
'''
can = Drinks('Cola', 3, "Cans" 375)
bottles = Drinks('Cola', 5, "Bottles", 600)
smlJuice = Drinks('Orange_Juice', 2, 'sml', 250)
medJuice = Drinks('Orange_Juice', 4, 'med', 450)

print(can.name)
'''
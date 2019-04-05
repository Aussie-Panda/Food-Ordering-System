from food import Food

class Drinks(Food):
	def __init__(self, name, price, volumn):
		super().__init__(name, price)
		self._price = price
		self._volumn = volumn


	@property
	def volumn(self):
		return self._volumn

	@volumn.setter
	def volumn(self, volumn):
		self._volumn = volumn

	@property
	def price(self):
		return self._price


	def computePrice(self):
		pass

can = Drinks('Lemonade(Can)', 3, 375)
bottles = Drinks('Lemonad(Bottles)', 5, 600)
smlJuice = Drinks('smlJuice', 2, 250)
medJuice = Drinks('medJuice', 4, 450)

print(can.name)
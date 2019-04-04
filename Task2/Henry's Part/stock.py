class Stock():
	def __init__(self):
		self._mains = {'buns': 0, 'patties': 0, 'wraps': 0}
		self._drinks = {'bottle': 0, 'can': 0, 'juice': 0}
		self._sides = {'smlFries': 0, 'medFries': 0, 'lrgFries': 0, 'smlNuggets': 0, 'lrgNuggets': 0}
		self._ingredients = {'tomato': 0, 'lettuce' : 0, 'cheddar_cheese' : 0, 'swiss_cheese' : 0, 'tomato_sauce' : 0}

	@property
	def mains(self):
		return self._mains

	@property
	def drinks(self):
		return self._drinks

	@property
	def sides(self):
		return self._sides
	
	@property
	def ingredients(self):
		return self._ingredients

	def addQuantity(self, item, amount):
		assert(item != None)
		assert(amount != None)

		if item in self._mains:
			self._mains[item] += amount
		elif item in self._drinks:
			self._drinks[item] += amount
		elif item in self._sides:
			self._sides[item] += amount
		elif item in self._ingredients:
			self._ingredients[item] += amount

	def decreaseQuantity(self, item, amount):
		assert(item != None)
		assert(amount != None)
class Stock():
	def __init__(self):
		self._mains = {'buns': 0, 'patties': 0, 'wraps': 0}
		self._drinks = {'bottle': 0, 'can': 0, 'juice': 0}
		self._sides = {'fries': 0, 'nuggets': 0}
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

	#method is add / subtract, item is a str and amount is int，size is str(sml,med,lrg)
	def changeQuantity(self, method, item, amount,size = None):
		assert(item != None)
		assert(amount != None)
		assert(method != None)
		if (method == 'add'):
			if item in self._mains.keys() :
				self._mains[item] += amount

			elif item in self._drinks.keys():
				if item == 'bottle':
					self._drinks['bottle'] += 600*amount
				elif item == 'can':
					self._drinks['can'] += 375*amount
				elif item == 'juice' and size == 'sml':
					self._drinks['juice'] += 250*amount
				elif item == 'juice' and size == 'lrg':
					self._drinks['juice'] += 450*amount

			elif item in self._sides.keys():
				if item == 'fries':
					if size == 'sml':
						self._sides['fries'] += 75*amount
					elif size == 'med':
						self._sides['fries'] += 125*amount
					elif size == 'lrg':
						self._sides['fries'] += 150*amount

				elif item == 'nuggets':
					if size == 'sml':
						self._sides['nuggets'] += 3*amount

					elif size == 'lrg':
						self._sides['nuggets'] += 6*amount

			elif item in self._ingredients.keys():
				self._ingredients[item] += amount
	

		elif(method == 'minus'):
			if item in self._mains.keys() :
				self._mains[item] -= amount

			elif item in self._drinks.keys():
				if item == 'bottle':
					self._drinks['bottle'] -= 600*amount
				elif item == 'can':
					self._drinks['can'] -= 375*amount
				elif item == 'juice' and size == 'sml':
					self._drinks['juice'] -= 250*amount
				elif item == 'juice' and size == 'lrg':
					self._drinks['juice'] -= 450*amount

			elif item in self._sides.keys():
				if item == 'fries':
					if size == 'sml':
						self._sides['fries'] -= 75*amount
					elif size == 'med':
						self._sides['fries'] -= 125*amount
					elif size == 'lrg':
						self._sides['fries'] -= 150*amount

				elif item == 'nuggets':
					if size == 'sml':
						self._sides['nuggets'] -= 3*amount

					elif size == 'lrg':
						self._sides['nuggets'] -= 6*amount

			elif item in self._ingredients.keys():
				self._ingredients[item] -= amount
'''
s = Stock()
s.changeQuantity('add', 'buns', 1)
s.changeQuantity('add', 'bottle', 1)
s.changeQuantity('add', 'can', 10)
s.changeQuantity('add', 'fries', 1, 'sml')
s.changeQuantity('add', 'nuggets', 1, 'lrg')
s.changeQuantity('add', 'juice', 1, 'lrg')



print(s._mains)
print(s._drinks)
print(s._sides)
print('======after minus=========')
s.changeQuantity('minus', 'buns', 1)
s.changeQuantity('minus', 'bottle', 1)
s.changeQuantity('minus', 'can', 10)
s.changeQuantity('minus', 'fries', 1, 'sml')
s.changeQuantity('minus', 'nuggets', 1, 'lrg')
s.changeQuantity('minus', 'juice', 1, 'lrg')
print(s._mains)
print(s._drinks)
print(s._sides)
'''
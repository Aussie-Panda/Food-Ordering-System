class StockError(Exception):
	
	def __init__(self, errors, msg=None):
		if msg is None:
			msg = "Those items are out of stock: %s"%(', '.join(errors))

		def __str__(self):
			return msg

		self._erros = errors


class QuantityError(Exception):
	def __init__(self,item):
		self._item = item

		def __str__(self):
			return f"Item {self._item} has invalid Quantity!"


'''
Check if a dictionary of food is out of stock
return value: None (void function)
'''
def checkStock(self, food):
	emptyFood = []

	for item in food.keys():
		if item.name in Stock.mains:
			if Stock.mains[item.name] < food[item]:
				emptyFood.append(item)

		elif item.name in Stock.drinks:
			if Stock.drinks[item.name] < food[item]:
				emptyFood.append(item)

		elif item.name in Stock.sides:
			if Stock.sides[item.name] < food[item]:
				emptyFood.append(item)

		elif item.name in Stock.ingredients:
			if Stock.ingredients[item.name] < food[item]:
				emptyFood.append(item)

	if emptyFood:
		raise StockError(emptyFood)
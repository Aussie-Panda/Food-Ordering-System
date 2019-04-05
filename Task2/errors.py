class StockError(Exception):
	
	def __init__(self, errors, msg=None):

		if msg is None:
			msg = "Those items are out of stock: %s"%(', '.join(errors))

		self._errors = errors

	def __str__(self):
		return msg

	@property
	def errors(self):
		return self._errors


class QuantityError(Exception):
	def __init__(self,item):
		self._item = item

		def __str__(self):
			return f"Item {self._item} has invalid Quantity!"


'''
Check if a dictionary of food is out of stock
return value: None (void function)
'''
def checkStock(food, stock):
	emptyFood = []

	for item in food.keys():
		if item.name in stock.mains:
			if stock.mains[item.name] < food[item]:
				emptyFood.append(item.name)

		elif item.name in stock.drinks:
			if stock.drinks[item.name] < food[item]:
				emptyFood.append(item.name)

		elif item.name in stock.sides:
			if stock.sides[item.name] < food[item]:
				emptyFood.append(item.name)

		elif item.name in stock.ingredients:
			if stock.ingredients[item.name] < food[item]:
				emptyFood.append(item.name)

	if emptyFood:
		raise StockError(emptyFood)
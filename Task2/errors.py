from mains import Mains, Burger, Wrap
from drinks import Drinks
from sides import Sides

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
	totalFood = {}
	# calculate total quantity/volumn for each type of food
	for item in food.keys():
		# for mains
		if isinstance(item, Mains):
			totalFood[item.name] = food[item]
			if isinstance(item, Burger):
				totalFood['buns'] =  item.numBun
				totalFood['patties'] = item.numPat
			elif isinstance(item, Wrap):
				totalFood['patties'] = item.numPat

			for i in item.ingredientsOrdered.keys():
				totalFood[i] = item.ingredientsOrdered[i]

		# for drinks
		elif isinstance(item, Drinks):
			if 'Juice' in item.name:
				totalFood[item.name] = food[item] * item.volumn
			else:
				target = f"{item.name}({item.size})"
				totalFood[target] = food[item]

		# for sides
		elif isinstance(item, Sides):
			if item.name not in totalFood:
				totalFood[item.name] = food[item] * item.volumn
			elif item.name in totalFood:
				totalFood[item.name] += food[item] * item.volumn

	# print(totalFood)
	for item in totalFood.keys():
		if item in stock.mains:
			if stock.mains[item] < totalFood[item]:
				emptyFood.append(item)

		elif item in stock.drinks:
			if stock.drinks[item] < totalFood[item]:
				emptyFood.append(item)

		elif item in stock.sides:
			if stock.sides[item] < totalFood[item]:
				emptyFood.append(item)

		elif item in stock.ingredients:
			if stock.ingredients[item] < totalFood[item]:
				emptyFood.append(item)
	
	if emptyFood:
		raise StockError(emptyFood)
	
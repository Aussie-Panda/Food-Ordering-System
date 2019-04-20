from src.mains import Mains, Burger, Wrap
from src.drinks import Drinks
from src.sides import Sides

# is raised when the food is out of stock
class StockError(Exception):
	def __init__(self, errors, msg=None):
		if msg is None:
			self._msg = "Those items are out of stock: %s"%(', '.join(errors))

		self._errors = errors

	def __str__(self):
		return self._msg

	@property
	def errors(self):
		return self._errors

# is raised when something cannot be found
class SearchError(Exception):
    def __init__(self, obj):
        self._obj=obj
    
    def __str__(self):
        msg = 'Sorry, ' + self._obj + ' is not found. Please try again.'
        return msg
    

'''
Check if a dictionary of food is out of stock
return value: a list of out-of-stock food
'''
def checkStock(food, stock):
	emptyFood = []
	totalFood = {}
	# calculate total quantity/volumn for each type of food
	for item in food.keys():
		# for mains
		if isinstance(item, Mains):
			totalFood[item.name] = food[item]
			for addOn in item.addOn.keys():
				if addOn not in totalFood:
					totalFood[addOn.lower()] = item.addOn[addOn]
				else:
					totalFood[addOn.lower()] += item.addOn[addOn]

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
		for category in stock.whole.values():
			if (item in category) and (category[item] < totalFood[item]):
				emptyFood.append(item)
	
	return emptyFood
	

from src.ordering_system import *
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
    


	

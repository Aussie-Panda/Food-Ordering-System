from food import Fßood

class Order():
	def __init__(self, orderId, food, orderStatus = "Not Submitted"):
		self._orderId = orderId 		# int
		self._orderedItem = food   		# dictionary
		self._orderStatus = orderStatus # string


	# compute total price of the order
	def computeNetPrice(self):
		totalPrice = 0
		for item in self.orderedItem.keys():
			thisPrice = item.price
			quantity = self.orderedItem[item]
			totalPrice += (thisPrice * quantity)

		return price

	
	# Funciton to modify the order
	def modifyOrder(self, item = None, value):
		assert(item != None)

		# If any invalid value is passed in, raise QuantityError. Errors should be catched outside
		if value < 0 or value == None:
			raise QuantityError(item)
			
		# 1. if item is in the order and value is set to 0, delete the item
		# 2. elif item is in the list and value is > 0, overwrite the previous value
		elif item in self.orderedItem and value != None:
			if value == 0:
				self.orderedItem.pop(item)
			else:
				self.orderedItem[item] = value

		# 3. elif item is not in the list, add item with value
		elif item not in self.orderedItem:
			if value == 0:
				raise QuantityError(item)
				
			self.orderedItem[item] = value

			


	# update orderStatus
	def updateOrder(self, status):
		self.orderStatus = status
		
	''' 
	Properties
	'''

	@property
	def orderId(self):
		return self._orderId
	
	@property
	def orderedItem(self):
		return self._orderedItem
	
	@property
	def orderStatus(self):
		return self._orderStatus
	

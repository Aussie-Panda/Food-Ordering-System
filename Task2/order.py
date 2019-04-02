from food import Food

class Order():
	def __init__(self, orderId, food, orderStatus = "Not Submitted"):
		self._orderId = orderId
		self._orderedItem = food
		self._orderStatus = orderStatus


	# compute total price of the order
	def computeNetPrice(self):
		price = 0
		for item in self.orderedItem:
			price += item.price

		return price


	# new food list will overwrite the old food list
	def modifyOrder(self, food = None):
		assert(food != None)
		self.orderedItem = food


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
	

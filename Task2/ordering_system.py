from Food import Food
from order import Order
from stock import Stock
from errors import StockError


class OrderingSystem():
	def __init__(self):
		self._id = 0
		self._order = []	# order's id should be in increasing order
		self._menu = []		# a list of all kind food


	def newId(self):
		self._id += 1
		return self._id

	def displayMenu(self):
		for item in self.menu:
			print(item)

	'''
	Check if item in food is out of stock. If yes, return None and errors; if no, create new order instance, 
	append it to order list and set status as "Pending"
	return value: order, [](if no StockError)/None, error list(if StockError)
	'''
	def makeOrder(self, food = None):
		
		assert(food != None)

		
		try:
			self.checkStock(food)

		except StockError as er:
			return None, er.errors

		newId = self.newId()
		new_order = Order(newID, food, "Pending")
		self.order.append(new_order)
		
		return new_order, []
			
	'''
	Check if a dictionary of food is out of stock
	return value: None (void function)
	'''
	def checkStock(self, food):
		emptyFood = []

		for item in food.keys():
			if item in Stock.mains:
				if Stock.mains[item] < food[item]:
					emptyFood.append(item)

			elif item in Stock.drinks:
				if Stock.drinks[item] < food[item]:
					emptyFood.append(item)

			elif item in Stock.sides:
				if Stock.sides[item] < food[item]:
					emptyFood.append(item)

			elif item in Stock.ingredients:
				if Stock.ingredients[item] < food[item]:
					emptyFood.append(item)

		if emptyFood:
			raise StockError(emptyFood)


	'''
	Ask for customer if they would like to enter email address and then send a receipt
	return value: None (void function)
	'''
	def sendReceipt(self,order):
		assert(order != None)
		send = input("Would you like to send a receit? (y/n): ")
		food = '\n'.join(order.orderedItem)
		receipt = f'----------\nDear customer,\nYour order has been confirmed.\nYour order ID is: {order.orderId}\nYour items are: \n{food}\n\nThank you for ordering!\n----------'

		if send == 'y':
			email = ""
			email += input("Please enter your email: ")
			
			while not email:
				email += input("Please enter your email: ")

			
			print("Your receipt has been sent to email " + email)
			print(receipt)


		else:
			print(receipt)


	'''
	Get next order either by status or particular id.
	return value: order (if found)/None(if not found)
	'''
	def getNextOrder(self, status = None, id = None):
		assert(status != None)

		if id is None:
			for i in self.order:
				if i.order.orderStatus == status:
					return i

		elif id is not None:
			for i in self.order:
				if i.order.orderId == id:
					return i

		return None		# if no order matches the requesting status or id

	'''
	Delete the next order that has requesting status or particular id
	return value: order (if found)/None(if not found)
	'''
	def deleteOrder(self, status = None, id = None):

		if id is None:
			for i in self.order:
				if i.order.orderStatus == status
					self.order.remove(i)
					return i

		elif id is not None:
			for i in self.order:
				if i.order.orderId == id:
					self.order.remove(i)
					return i

		return None		# if no order matches the requesting status or id
		

	'''
	Properties
	'''

	@property
	def order(self):
		return self._order

	
	@property
	def menu(self):
		return self._menu
	
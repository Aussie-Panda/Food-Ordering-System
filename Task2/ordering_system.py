from food import Food
from order import Order
# from stock import Stock
from errors import StockError, QuantityError


class OrderingSystem():
	def __init__(self):
		self._id = 0
		self._order = []	# a list of Order. order's id should be in increasing order
		self._menu = []		# a list of all kind food


	def newId(self):
		self._id += 1
		return self._id

	def displayMenu(self):
		print("--------MENU--------")
		for item in self.menu:
			print(item)
		print("-------End of Menu-------")

	def getFood(self,name):
		for i in self.menu:
			if i.name == name:
				return i
		return None

	'''
	Check if item in food is out of stock. If yes, return None and errors; if no, create new order instance, 
	append it to order list and set status as "Pending"
	return value: order, [](if no StockError)/None, error list(if StockError)
	'''
	def makeOrder(self, food = None):
		
		assert(food != None)

		'''
		try:
			self.checkStock(food)

		except StockError as er:
			return None, er.errors
		'''
		newId = self.newId()
		new_order = Order(newId, food, "Pending")
		# print(new_order)
		self.order.append(new_order)
		
		price = new_order.computeNetPrice()
		print(f"Thank you, your order has been made.\nTotal Price: ${price}")
		
		return new_order, []
			
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


	'''
	Ask for customer if they would like to enter email address and then send a receipt
	return value: None (void function)
	'''
	def sendReceipt(self,order):
		assert(order != None)
		send = 'n'
		# send = input("Would you like to send a receit? (y/n): ")
		'''
		price = order.computeNetPrice
		receipt = f'------Receipt-----\nDear customer,\nYour order has been confirmed.\nYour order ID is: {order.orderId}\nYour items are: \n{food}\nTotal Price: ${price}\nThank you for ordering!\n--------End of Receipt-------'
		'''
		receipt = f'---------Receipt--------\n{order}\n--------End of Receipt--------'
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

		if id is None:
			for i in self.order:
				if i.orderStatus == status:
					return i

		elif id is not None:
			for i in self.order:
				if i.orderId == id:
					return i

		return None		# if no order matches the requesting status or id

	'''
	Delete the next order that has requesting status or particular id
	return value: order (if found)/None(if not found)
	'''
	def deleteOrder(self, status = None, id = None):

		if id is None:
			for i in self.order:
				if i.orderStatus == status:
					self.order.remove(i)
					return i

		elif id is not None:
			for i in self.order:
				if i.orderId == id:
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
	